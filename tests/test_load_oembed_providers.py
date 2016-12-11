import pathlib
import pytest
from pytest_shutil import env
from aiounfurl.parsers import oembed


def test_oembed_providers_loaded():
    providers = oembed.load_providers()
    assert isinstance(providers, list)
    assert len(providers) == 0


def test_oembed_load_exception():
    with env.set_env(oembed.OEMBED_PROVIDERS_ENV_VAR_NAME, 'test.json'):
        with pytest.raises(oembed.LoadOembedProvidersException):
            oembed.load_providers()


def test_oembed_provider_processes():
    providers_filepath = pathlib.Path(__file__).parent / 'files' / 'test_providers.json'
    with env.set_env(oembed.OEMBED_PROVIDERS_ENV_VAR_NAME, providers_filepath):
        providers = oembed.load_providers()
    processed_providers = oembed.prepare_providers(providers)
    assert isinstance(processed_providers, list)
    assert len(providers) == len(processed_providers)
