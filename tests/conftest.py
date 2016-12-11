import pathlib
import pytest
from pytest_shutil import env
from aiounfurl.parsers import oembed


@pytest.fixture(scope='module')
def files_dir():
    return pathlib.Path(__file__).parent / 'files'


@pytest.fixture(scope='module')
def oembed_providers(files_dir):
    providers_filepath = str(files_dir / 'test_providers.json')
    with env.set_env(oembed.OEMBED_PROVIDERS_ENV_VAR_NAME, providers_filepath):
        return oembed.prepare_providers(oembed.load_providers())
