import pathlib
import asyncio
import aiohttp
from marshmallow import Schema, fields, ValidationError
from aiohttp.web import Application, json_response, run_app, Response
from aiounfurl import exceptions
from aiounfurl.parsers.oembed import providers_helpers
from aiounfurl.views import get_preview_data, fetch_all


home_content = (pathlib.Path(__file__).parent / 'index.html').read_text()


def _validate_resolution(value):
    if value < 1:
        raise ValidationError('Value must be greater than 0.')
    if value > 3000:
        raise ValidationError('Value must not be lesser than 3000.')


class RequestParamsSchema(Schema):
    url = fields.Url(required=True)
    maxwidth = fields.Integer(required=False, validate=_validate_resolution)
    maxheight = fields.Integer(required=False, validate=_validate_resolution)


async def _base_view(request, func):
    params, errors = RequestParamsSchema().load(request.rel_url.query)
    if errors:
        return json_response(errors, status=400)
    app = request.app
    async with aiohttp.ClientSession(loop=app.loop) as session:
        oembed_params = {k: v for k, v in params.items() if k != 'url'}
        try:
            result = await func(
                session,
                params['url'],
                loop=app.loop,
                oembed_providers=app['providers'],
                oembed_params=oembed_params)
        except exceptions.BaseAiounfurlException as exc:
            return json_response({'error': str(exc)}, status=400)
        return json_response(result)


async def extract(request):
    return await _base_view(request, fetch_all)


async def preview(request):
    return await _base_view(request, get_preview_data)


async def home(request):
    return Response(text=home_content, content_type='text/html')


async def init(loop):
    app = Application(loop=loop)
    app.router.add_get('/', home)
    app.router.add_get('/extract', extract)
    app.router.add_get('/preview', preview)
    return app


loop = asyncio.get_event_loop()
app = loop.run_until_complete(init(loop))
app['providers'] = providers_helpers.prepare_providers(
    providers_helpers.load_providers())
run_app(app)
