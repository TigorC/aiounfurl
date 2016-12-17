def extract_from_html(soup):
    meta = soup.findAll('meta')
    result = {}
    for tag in meta:
        if tag.has_attr('name') and 'twitter:' in tag['name']:
            tag_name = tag['name']
            property_name = tag_name.replace('twitter:', '', 1).replace(':', '_')
            result[property_name] = tag['content']
    return result
