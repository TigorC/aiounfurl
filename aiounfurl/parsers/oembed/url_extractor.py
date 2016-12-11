from collections import OrderedDict
from urllib.parse import urlsplit, urlunsplit, urlencode, parse_qsl


class OEmbedURLExtractor(object):

    MIME_TYPES = [
        'application/json+oembed',
        'text/xml+oembed']

    def __init__(self, providers, params=None):
        self._providers = providers
        self._params = params

    def _build_oembed_url(self, url, provider, data_format):
        endpoint_url = provider['url'].replace('{format}', data_format)
        scheme, netloc, path, qs, fragment = urlsplit(endpoint_url)
        query_params = OrderedDict(parse_qsl(qs))
        query_params['url'] = url
        query_params['format'] = data_format
        if self._params:
            query_params.update(self._params)
        query_params = urlencode(query_params, True)
        return urlunsplit((scheme, netloc, path, query_params, fragment))

    def get_oembed_url(self, url, data_format='json'):
        for provider in self._providers:
            for schema_re in provider['schemes']:
                if schema_re.match(url):
                    return self._build_oembed_url(url, provider, data_format)

    def get_oembed_url_from_html(self, soup):
        """
        oEmbed providers can choose to make their oEmbed support discoverable
        by adding elements to the head of their existing (X)HTML documents.
        """
        for mime_type in self.MIME_TYPES:
            link = soup.find('link', type=mime_type, href=True)
            if link:
                return link['href']
