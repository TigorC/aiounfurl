META_TAGS_NAMES = [
    'keywords',
    'description',
    'subject',
    'copyright',
    'language',
    'Classification',
    'author',
    'pagename',
    'subtitle',
    'date',
    'syndication-source',
    'original-source']


def extract_from_html(soup):
    meta = soup.findAll('meta')
    result = {}
    for tag in meta:
        attrs = tag.attrs
        has_required_attrs = 'name' in attrs and 'content' in attrs
        if has_required_attrs and attrs['name'] in META_TAGS_NAMES:
            result[attrs['name']] = attrs['content']
    return {k: v for k, v in result.items() if v}
