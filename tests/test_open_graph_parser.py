from bs4 import BeautifulSoup
from aiounfurl.parsers import open_graph


def test_without_og_tags(files_dir):
    html = (files_dir / 'oembed_json.html').read_text()
    result = open_graph.extract_from_html(BeautifulSoup(html))
    assert result == {}


def test_extract_flat_data(files_dir):
    html = (files_dir / 'og.html').read_text()
    result = open_graph.extract_from_html(BeautifulSoup(html))
    assert 'title' in result
    assert result['title'] == 'The Rock'


def test_extract_arrays(files_dir):
    html = (files_dir / 'og.html').read_text()
    result = open_graph.extract_from_html(BeautifulSoup(html))
    assert 'image' in result
    assert isinstance(result['image'], list)
    assert len(result['image']) == 3
