def extract(soup):
    result = {}
    for header_lvl in range(1, 4):
        header = soup.find('h{0}'.format(header_lvl))
        if header and header.text:
            result['title'] = header.text
            first_p = header.find_next('p')
            if (first_p and first_p.text != ''):
                result['description'] = first_p.text
            first_image = header.find_next_sibling('img')
            if first_image and first_image['src'] != '':
                result['image'] = first_image['src']
            break
    return result
