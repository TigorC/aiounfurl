def _add_to_result(result, property_name_parts, content):
    if len(property_name_parts) > 1:
        return result
    property_name = property_name_parts[0]
    if property_name in result.keys():
        if isinstance(result[property_name], list):
            result[property_name].append(content)
        else:
            result[property_name] = [result[property_name], content]
    else:
        result[property_name] = content
    return result


def extract_from_html(soup):
    meta = soup.findAll('meta')
    result = {}
    for tag in meta:
        if tag.has_attr('property') and 'og:' in tag['property']:
            tag_property = tag['property']
            property_name_parts = tag_property.replace('og:', '', 1).split(':')
            result = _add_to_result(result, property_name_parts, tag['content'])
    return result
