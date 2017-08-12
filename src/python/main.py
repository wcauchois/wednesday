import asyncio
from aiohttp import web
import aiopg
from aiopg.sa import create_engine
import aiohttp_jinja2
import jinja2
import yaml
import logging
from aiohttp import WSMsgType
import json
import uuid

from utils import get_db_url
from models import Post

tbl = Post.__table__


logger = logging.getLogger(__name__)


class RootView(web.View):
  @aiohttp_jinja2.template('index.html')
  async def get(self):
    return {} # Template params

def get_uuid():
  return uuid.uuid1()

class ConnectedClient(object):
  def __init__(self, socket):
    self.id = get_uuid()
    self.socket = socket

  def __cmp__(self, other):
    return cmp(self.id, other.id)

class RpcException(Exception):
  pass

class RpcMethods(object):
  @staticmethod
  async def test(req, args):
    ret = {'hello': 'world'}
    if len(args) > 0:
      ret['args'] = args
    return ret

  @staticmethod
  async def will_always_throw(req, args):
    raise RpcException('This is an exception!')

  @staticmethod
  async def add_post(req, args):
    async with req.app['db'].acquire() as conn:
      res = await conn.execute(tbl.insert().values(**args[0]))
      row = await res.first()
      return dict(row)

class WebSocketView(web.View):
  async def get_response_from_rpc_call(self, payload):
    method_name = payload['method']
    call_id = payload['call_id']
    arguments = payload.get('arguments', [])
    func = getattr(RpcMethods, method_name)
    try:
      if func is not None:
        ret = await func(self.request, arguments)
        response = {'type': 'rpc_success', 'return_value': json.dumps(ret)}
      else:
        raise RpcException('Unknown method: {}'.format(method_name))
    except RpcException as e:
      response = {'type': 'rpc_error', 'message': str(e)}
    response['call_id'] = call_id
    return response

  async def get(self):
    ws = web.WebSocketResponse()
    await ws.prepare(self.request)
    logger.info('WebSocket client connected')
    client = ConnectedClient(ws)
    self.request.app['connected_clients'].append(client)
    # Could get variables from session here for auth etc
    async for msg in ws:
      if msg.type == WSMsgType.TEXT:
        logger.info('Got WebSocket data: {}'.format(msg.data))
        payload = json.loads(msg.data)
        if payload['type'] == 'rpc':
          response = await self.get_response_from_rpc_call(payload)
          ws.send_json(response)
      elif msg.type == WSMsgType.ERROR:
        logger.error('WebSocket error: {}'.format(ws.exception()))
    logger.info('WebSocket connection closed')
    self.request.app['connected_clients'].remove(client)
    return ws

app = web.Application()
app.router.add_static('/dist', './dist')
app.router.add_get('/ws', WebSocketView)
# This should go last since it wildcard matches on any route.
app.router.add_get('/{rest:.*}', RootView)

app['connected_clients'] = []

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

async def setup_postgres_pool():
  app['db'] = await create_engine(get_db_url())
  logger.info("Created PSQL engine")

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  loop = asyncio.get_event_loop()
  loop.run_until_complete(setup_postgres_pool())
  web.run_app(app)

