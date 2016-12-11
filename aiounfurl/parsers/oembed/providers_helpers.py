import os
import re
import json
from aiounfurl.exceptions import BaseAiounfurlException


OEMBED_PROVIDERS_ENV_VAR_NAME = 'OEMBED_PROVIDERS_FILE'


class LoadOembedProvidersException(BaseAiounfurlException):
    pass


def schema_mask_to_re(url_schema):
    schema_re = r'.*'.join(map(re.escape, url_schema.split('*')))
    return re.compile(r'^{0}$'.format(schema_re))


def load_providers():
    """
    Format file must be json
    example you can find here http://oembed.com/providers.json
    """
    providers_filepath = os.getenv(OEMBED_PROVIDERS_ENV_VAR_NAME)
    if not providers_filepath:
        return []
    try:
        providers_file = open(providers_filepath)
    except IOError as e:
        msg = "Error loading Oembed providers, I/O error ({0}): {1}"
        raise LoadOembedProvidersException(msg.format(e.errno, e.strerror))
    else:
        providers = json.load(providers_file)
        providers_file.close()
    return providers


def prepare_providers(providers):
    result = []
    for provider in providers:
        endpoints = provider.get('endpoints', [])
        for index, endpoint in enumerate(endpoints):
            schemes = endpoint.get('schemes')
            endpoint_url = endpoint.get('url')
            if schemes and endpoint_url:
                result.append({
                    'provider_name': provider['provider_name'],
                    'schemes': [schema_mask_to_re(s) for s in schemes],
                    'url': endpoint_url})
    return result
