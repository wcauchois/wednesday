import asyncio
from aiohttp import web
import aiopg
import aiohttp_jinja2
import jinja2
import yaml
import logging
from aiohttp import WSMsgType

logger = logging.getLogger(__name__)

config = yaml.load(open('config.yml'))
db_conf = config['database']
dsn = 'dbname={} user={} password={} host={}'.format(
  db_conf['dbname'], db_conf['user'], db_conf['password'], db_conf['host'])

class RootView(web.View):
  @aiohttp_jinja2.template('index.html')
  async def get(self):
    return {} # Template params

class WebSocketView(web.View):
  async def get(self):
    ws = web.WebSocketResponse()
    await ws.prepare(self.request)
    logger.info('WebSocket client connected')
    # Could get variables from session here for auth etc
    async for msg in ws:
      if msg.type == WSMsgType.TEXT:
        logger.info('Got WebSocket data: {}'.format(msg.data))
      elif msg.type == WSMsgType.ERROR:
        logger.error('WebSocket error: {}'.format(ws.exception()))
    logger.info('WebSocket connection closed')
    return ws

async def setup_postgres_pool():
  global pool
  pool = await aiopg.create_pool(dsn)
  logger.info("Created PSQL pool")

app = web.Application()
app.router.add_static('/dist', './dist')
app.router.add_get('/ws', WebSocketView)
# This should go last since it wildcard matches on any route.
app.router.add_get('/{rest:.*}', RootView)

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  loop = asyncio.get_event_loop()
  loop.run_until_complete(setup_postgres_pool())
  web.run_app(app)

