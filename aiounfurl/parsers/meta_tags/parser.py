from . import headers_tags, html5_semantic_tags, semantic_tags


def extract_from_html(soup):
    result = {}
    parsers = [
        semantic_tags,
        html5_semantic_tags,
        headers_tags]
    for parser in parsers:
        result.update(parser.extract(soup))
    return {k: v for k, v in result.items() if v}
