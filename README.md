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
Full example you can find [here](https://github.com/TigorC/aiounfurl/blob/master/example/srv.py).

## Tests
Install the `tox` package and run command:

```bash
tox
```