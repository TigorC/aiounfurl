def generate_accept_language(languages):
    if languages is None:
        return None
    result = []
    for index, lang in enumerate(languages):
        result.append({'code': lang, 'weight': 0.9 - index * 0.1})
    return ', '.join(['{code};q={weight}'.format_map(l) for l in result])


def generate_headers(languages=None):
    headers = {}
    accept_language = generate_accept_language(languages)
    if accept_language:
        headers['Accept-Language'] = accept_language
    return headers or None
