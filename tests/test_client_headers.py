from aiounfurl.headers_utils import generate_accept_language, generate_headers


def test_generate_accept_language():
    languages = ['ru-RU', 'ru', 'en-US', 'en']
    result = generate_accept_language(languages)
    assert result == 'ru-RU;q=0.9, ru;q=0.8, en-US;q=0.7, en;q=0.6'


def test_blank_languages():
    assert generate_accept_language([]) == ''


def test_generate_headers():
    languages = []
    assert generate_headers(languages) is None
