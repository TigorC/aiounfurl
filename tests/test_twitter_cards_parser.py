from bs4 import BeautifulSoup
from aiounfurl.parsers import twitter_cards


def test_extract_flat_data(files_dir):
    html = (files_dir / 'twitter_cards.html').read_text()
    result = twitter_cards.extract_from_html(BeautifulSoup(html))
    assert 'title' in result
    assert result['title'] == 'The Rock'
