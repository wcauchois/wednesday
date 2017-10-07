import asyncio
from aiohttp import web
import jinja2
import aiohttp_jinja2

from views import RootView, WebSocketView, DebugView
from database import Database
from pubsub import PubSub


app = web.Application()
app.router.add_static('/dist', './dist')
app.router.add_static('/static', './static')
app.router.add_get('/ws', WebSocketView)
app.router.add_get('/_debug', DebugView)

# This should go last since it wildcard matches on any route.
app.router.add_get('/{rest:.*}', RootView)

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

services = {
  'db': Database(app),
  'ps': PubSub(app),
}

def get_sorted_services():
  return sorted(services.values(), key=lambda s: s.init_order)

app['clients'] = {}
app.update(services)

async def on_startup(app):
  for service in get_sorted_services():
    await service.startup()

# http://aiohttp.readthedocs.io/en/stable/web.html#graceful-shutdown
async def on_shutdown(app):
  await asyncio.gather(*[client.close() for client in app['clients'].values()])
  for service in reversed(get_sorted_services()):
    await service.shutdown()

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
