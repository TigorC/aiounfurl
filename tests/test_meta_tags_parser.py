from bs4 import BeautifulSoup
from aiounfurl.parsers import meta_tags


def test_extraction(files_dir):
    html = (files_dir / 'meta_tags.html').read_text()
    result = meta_tags.extract_from_html(BeautifulSoup(html))
    assert 'description' in result.keys()
    assert result['description'] == '150 words'
    assert 'unknowntag' not in result.keys()
