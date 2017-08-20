from aiohttp import web
import jinja2
import aiohttp_jinja2

from views import RootView, WebSocketView
from database import Database
from pubsub import PubSub


app = web.Application()
app.router.add_static('/dist', './dist')
app.router.add_get('/ws', WebSocketView)
# This should go last since it wildcard matches on any route.
app.router.add_get('/{rest:.*}', RootView)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

app['clients'] = set()
app['db'] = Database()
app['ps'] = PubSub()

async def on_startup(app):
  await app['db'].startup()
  await app['ps'].startup()

# http://aiohttp.readthedocs.io/en/stable/web.html#graceful-shutdown
async def on_shutdown(app):
  for client in app['clients']:
    await client.socket.close(code=WSCloseCode.GOING_AWAY)
  await app['db'].shutdown()
  await app['ps'].shutdown()

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
