import asyncio
from bs4 import BeautifulSoup
from aiounfurl.parsers import oembed, open_graph, meta_tags, twitter_cards


async def _fetch_oembed(session, url):
    async with session.get(url) as resp:
        return await resp.json()


async def _fetch_data(session, url, oembed_url_extractor=None):
    result = {}
    async with session.get(url) as resp:
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
        oembed_result, other_results = await asyncio.gather(*tasks, loop=loop)
        result['oembed'] = oembed_result
        result.update(other_results)
    else:
        other_results = await _fetch_data(session, url, oembed_url_extractor)
        result.update(other_results)
    return result
