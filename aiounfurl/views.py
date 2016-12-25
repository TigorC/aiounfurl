import asyncio
import aiohttp
from bs4 import BeautifulSoup
from aiounfurl import exceptions
from aiounfurl.parsers import oembed, open_graph, meta_tags, twitter_cards


OK_STATUS_CODE = 200


async def _fetch_oembed(session, url):
    async with session.get(url) as resp:
        if resp.status != OK_STATUS_CODE:
            msg = 'Error getting oembed for endpoint {0}, status_code: {1}'
            msg = msg.format(url, resp.status)
            raise exceptions.InvalidOEmbedEndpoint(msg)
        return await resp.json()


async def _fetch_page_html(session, url):
    async with session.get(url) as resp:
        if resp.status != OK_STATUS_CODE:
            msg = 'Error getting data for url {0}, status_code: {1}'.format(
                url, resp.status)
            raise exceptions.InvalidURLException(msg)
        return await resp.text()


async def _fetch_data(session, url, oembed_url_extractor=None):
    result = {}
    try:
        html = await _fetch_page_html(session, url)
    except aiohttp.errors.ClientError as exc:
        msg = 'Error getting page {0}, exception: {1}'.format(
            url, str(exc))
        raise exceptions.FetchPageException(msg)
    soup = BeautifulSoup(html, 'html5lib')
    if oembed_url_extractor:
        oembed_url = oembed_url_extractor.get_oembed_url_from_html(soup)
        if oembed_url:
            result['oembed'] = await _fetch_oembed(session, oembed_url)
    result['open_graph'] = open_graph.extract_from_html(soup)
    result['twitter_cards'] = twitter_cards.extract_from_html(soup)
    result['meta_tags'] = meta_tags.extract_from_html(soup)
    return result


async def fetch_all(session, url, loop=None, oembed_providers=None,
                    oembed_params=None):
    oembed_url_extractor = oembed.OEmbedURLExtractor(
        oembed_providers or [], params=oembed_params)
    oembed_url = oembed_url_extractor.get_oembed_url(url)

    result = {}
    if oembed_url:
        tasks = [
            _fetch_oembed(session, oembed_url),
            _fetch_data(session, url)]
        oembed_result, other_results = await asyncio.gather(
            *tasks, loop=loop, return_exceptions=True)
        raise_exceptions = (
            exceptions.InvalidURLException,
            exceptions.FetchPageException)
        if isinstance(other_results, raise_exceptions):
            raise other_results
        if isinstance(oembed_result, dict):
            result['oembed'] = oembed_result
        elif isinstance(oembed_result, exceptions.InvalidOEmbedEndpoint):
            result['oembed'] = {
                'error': str(oembed_result)}
        result.update(other_results)
    else:
        other_results = await _fetch_data(session, url, oembed_url_extractor)
        result.update(other_results)
    return result


async def get_preview_data(session, url, loop=None, oembed_providers=None,
                           oembed_params=None):
    data = await fetch_all(
        session,
        url,
        loop=loop,
        oembed_providers=oembed_providers,
        oembed_params=oembed_params)
    result = {'title': None, 'description': None, 'image': None}
    sources = ['oembed', 'open_graph', 'twitter_cards', 'meta_tags']
    for field in ['title', 'description']:
        for source in sources:
            result[field] = data.get(source, {}).get(field)
            if result[field]:
                break
        result[field] = result[field] or None

    # oembed image
    if data.get('oembed'):
        if data['oembed']['type'] == 'photo':
            result['image'] = data['oembed'].get('url')
        elif data['oembed'].get('thumbnail_url'):
            result['image'] = data['oembed']['thumbnail_url']

    # open graph image
    if not result['image'] and data.get('open_graph'):
        image = data['open_graph'].get('image')
        if image and isinstance(image, list):
            result['image'] = image[0]
        elif image:
            result['image'] = image

    # twitter cards image
    if not result['image'] and data.get('twitter_cards'):
        result['image'] = data['twitter_cards'].get('image')

    # from meta tags
    if not result['image'] and data.get('meta_tags'):
        result['image'] = data['meta_tags'].get('image') or None
    return result
