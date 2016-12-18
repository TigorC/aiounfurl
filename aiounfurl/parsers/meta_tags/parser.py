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


def _get_title(soup):
    if (soup.title and soup.title.text != ''):
        return soup.title.text
    if (soup.h1 and soup.h1.text != ''):
        return soup.h1.text
    return None


def _get_description(soup):
    first_h1 = soup.find('h1')
    if first_h1:
        first_p = first_h1.find_next('p')
        if (first_p and first_p.string != ''):
            return first_p.text
    first_p = soup.find('p')
    if (first_p and first_p.string != ''):
        return first_p.string
    return None


def _get_image(soup):
    first_h1 = soup.find('h1')
    if first_h1:
        first_image = first_h1.find_next_sibling('img')
        if first_image and first_image['src'] != '':
            return first_image['src']
    return None


def extract_from_html(soup):
    meta = soup.findAll('meta')
    result = {}
    for tag in meta:
        attrs = tag.attrs
        has_required_attrs = 'name' in attrs and 'content' in attrs
        if has_required_attrs and attrs['name'] in META_TAGS_NAMES:
            result[attrs['name']] = attrs['content']
    result['title'] = _get_title(soup)
    if not result.get('description'):
        result['description'] = _get_description(soup)
    result['image'] = _get_image(soup)
    return {k: v for k, v in result.items() if v}
