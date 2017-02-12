[![Build Status](https://travis-ci.org/TigorC/aiounfurl.svg?branch=master)](https://travis-ci.org/TigorC/aiounfurl)
[![Coverage Status](https://coveralls.io/repos/github/TigorC/aiounfurl/badge.svg?branch=master)](https://coveralls.io/github/TigorC/aiounfurl?branch=master)

## aiounfurl
Using this library you can extract meta information from web pages and create site preview.
The library uses four sources of information:

1. [oEmbed](http://oembed.com)
2. [Open Graph](http://ogp.me)
3. [Twitter Cards](https://dev.twitter.com/cards/overview)
4. HTML meta tags

## Requirements
* python 3.5
* aiohttp
* beautifulsoup4
* html5lib

## Installation
```bash
pip install aiounfurl
```

## Example of using

To extract all site data:

```python
import asyncio
import aiohttp
from pprint import pprint
from aiounfurl.views import get_preview_data, fetch_all


async def get_links_data(links, loop):
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_all(session, l, loop) for l in links]
        results = await asyncio.gather(*tasks, loop=loop, return_exceptions=True)
    return [{'link':l, 'data': d} for l, d in zip(links, results)]


links = [
    'https://habrahabr.ru/post/314606/',
    'https://www.youtube.com/watch?v=9EftQMnuhvU',
    'https://medium.freecodecamp.com/million-requests-per-second-with-python-95c137af319'
]
loop = asyncio.get_event_loop()
result = loop.run_until_complete(get_links_data(links, loop))
loop.close()
pprint(result)
```

## Server example.
Full example you can find [here](https://github.com/TigorC/aiounfurl/blob/master/example/srv.py).

Install required packages for running example:

```bash
pip install -r example/requirements.txt
```
Run `python srv.py runserver`, then open http://127.0.0.1:8080/

## Running the example in Docker

I added a docker image with the example in http://hub.docker.com/ to run the sample as a separate independent service.

Running in the background:

```bash
docker run --name aiounfurl -p 8080:8080 -d tigorc/aiounfurl
```

then you can open our example [http://127.0.0.1:8080/](http://127.0.0.1:8080/).

Using the list of oEmbed providers (a json file with a list of providers /path_to_file/providers.json has to be preliminarily created):

```bash
docker run --name aiounfurl -p 8080:8080 -e "OEMBED_PROVIDERS_FILE=/srv/app/providers.json" -v /path_to_file/providers.json:/srv/app/providers.json -d tigorc/aiounfurl
```

## Tests
Install the `tox` package and run command:

```bash
tox
```
