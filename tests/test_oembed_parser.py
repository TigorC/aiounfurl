from bs4 import BeautifulSoup
from aiounfurl.parsers import oembed


def test_oembed_not_match(oembed_providers):
    oembed_url_extractor = oembed.OEmbedURLExtractor(oembed_providers)
    url = 'http://test.com'
    assert oembed_url_extractor.get_oembed_url(url) is None


def test_oembed_founded(oembed_providers):
    oembed_url_extractor = oembed.OEmbedURLExtractor(oembed_providers)
    url = 'https://www.instagram.com/p/BNHh2YJDdcY/'
    oembed_url = oembed_url_extractor.get_oembed_url(url)
    assert isinstance(oembed_url, str)


def test_oembed_discovery(oembed_providers, files_dir):
    oembed_html = (files_dir / 'oembed_json.html').read_text()
    soup = BeautifulSoup(oembed_html)
    oembed_url_extractor = oembed.OEmbedURLExtractor(oembed_providers)
    oembed_url = oembed_url_extractor.get_oembed_url_from_html(soup)
    assert isinstance(oembed_url, str)


def test_oembed_params(oembed_providers):
    oembed_url_extractor = oembed.OEmbedURLExtractor(
        oembed_providers, params={'maxwidth': 200})
    url = 'https://www.instagram.com/p/BNHh2YJDdcY/'
    oembed_url = oembed_url_extractor.get_oembed_url(url)
    assert isinstance(oembed_url, str)
    assert 'maxwidth=200' in oembed_url
