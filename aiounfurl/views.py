import asyncio
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


async def _fetch_data(session, url, oembed_url_extractor=None):
    result = {}
    async with session.get(url) as resp:
        if resp.status != OK_STATUS_CODE:
            msg = 'Error getting data for url {0}, status_code: {1}'.format(
                url, resp.status)
            raise exceptions.InvalidURLException(msg)
        html = await resp.text()
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
        if isinstance(other_results, exceptions.InvalidURLException):
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
