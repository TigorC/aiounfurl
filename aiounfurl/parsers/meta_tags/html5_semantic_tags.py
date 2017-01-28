def extract(soup):
    result = {}
    article_tags = soup.find_all('article') or []
    if len(article_tags) != 1:
        return result
    article = article_tags[0]
    first_h1 = article.find('h1')
    if first_h1 and first_h1.text:
        result['title'] = first_h1.text
    description = article.find('p')
    if description and description.text:
        result['description'] = description.text
    first_image = article.find('img')
    if first_image and first_image['src'] != '':
        result['image'] = first_image['src']
    return result
