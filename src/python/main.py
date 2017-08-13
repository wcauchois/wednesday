import asyncio
from aiohttp import web
import aiopg
from aiopg.sa import create_engine
import aiohttp_jinja2
import jinja2
import yaml
import logging
from aiohttp import WSMsgType, WSCloseCode
import json
import uuid
from graph_store import GraphStore, NodeValue, Node
from collections import defaultdict

from utils import get_db_url, remove_null_values, unix_time_seconds
from models import Post, post_table


logger = logging.getLogger(__name__)
queue = asyncio.Queue()


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
    self.post_graph = GraphStore()

  def __cmp__(self, other):
    return cmp(self.id, other.id)

class PostValue(NodeValue):
  def __init__(self, id, created, parent_id, content):
    self.id = id
    self.created = created
    self.parent_id = parent_id
    self.content = content

  def serialize(self):
    return remove_null_values({
      'id': self.id,
      'created': self.created and unix_time_seconds(self.created),
      'parent_id': self.parent_id,
      'content': self.content
    })

def topo_sort(posts):
  # Based on https://en.wikipedia.org/wiki/Topological_sorting#Kahn.27s_algorithm
  result = []
  parent_id_to_post_map = defaultdict(list)
  for post in posts:
    parent_id_to_post_map[post.parent_id].append(post)
  working_set = parent_id_to_post_map.get(None, []) # Nodes which have no parent.
  while len(working_set) > 0:
    cur = working_set.pop()
    result.append(cur)
    if cur.parent_id is not None:
      for child in parent_id_to_post_map.get(cur.parent_id, []):
        working_set.append(child)
  return result

async def convert_posts_into_graph_store(app):
  "Convert the entire posts table into a GraphStore. This will not scale."
  async with app['db'].acquire() as conn:
    rows = conn.execute(post_table.select())
    post_list = []
    async for row in rows:
      post_list.append(PostValue(**dict(row.items())))
    sorted_posts = topo_sort(post_list)
    g = GraphStore()
    for post in sorted_posts:
      node_from_post = Node(post.id, post)
      g = g.add_node(post.parent_id or Node.ROOT_ID, node_from_post)
    return g

class RpcMethods(object):
  @staticmethod
  async def test(req, args):
    ret = {'hello': 'world'}
    if len(args) > 0:
      ret['args'] = args
    return ret

  @staticmethod
  async def will_always_throw(req, args):
    raise Exception('This is an exception!')

  @staticmethod
  async def add_post(req, args):
    async with req.app['db'].acquire() as conn:
      param = args[0]
      values = remove_null_values({
        'parent_id': param.get('parent_id'),
        'content': param.get('content')
      })
      insert_result = await conn.execute(post_table.insert().values(**values))
      row = await insert_result.first()
      select_result = await conn.execute(
        post_table.select().where(post_table.c.id == row['id']))
      post_row = await select_result.first()
      # NOTE(wcauchois): Is this really the only way to convert the result to the ORM model??
      post = Post(**dict(post_row.items()))
      return post.to_json()

  # SOON TO BE DEPRECATED FOR GRAPH SYNCING
  @staticmethod
  async def all_posts(req, args):
    async with req.app['db'].acquire() as conn:
      result = conn.execute(post_table.select().order_by(post_table.c.created))
      post_json_list = []
      async for row in result:
        post = Post(**dict(row.items()))
        post_json_list.append(post.to_json())
      return {'posts': post_json_list}

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
    except Exception as e:
      logging.exception('RPC exception') # Prints traceback
      response = {'type': 'rpc_error', 'message': str(e)}
    response['call_id'] = call_id
    return response

  async def send_initial_graph_sync(self):
    g = await convert_posts_into_graph_store(self.request.app)
    self.client.post_graph = g
    self.client.socket.send_json({
      'type': 'sync_graph',
      'graph': g.serialize()
    })

  async def get(self):
    ws = web.WebSocketResponse()
    await ws.prepare(self.request)
    logger.info('WebSocket client connected')
    self.client = ConnectedClient(ws)
    self.request.app['connected_clients'].append(self.client)
    # Could get variables from session here for auth etc
    asyncio.ensure_future(self.send_initial_graph_sync()) # Background
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
    self.request.app['connected_clients'].remove(self.client)
    return ws

async def queue_worker(app):
  while True:
    item = await queue.get()
    logger.info('Processing queue message')
    if item is None:
      break

app = web.Application()
app.router.add_static('/dist', './dist')
app.router.add_get('/ws', WebSocketView)
# This should go last since it wildcard matches on any route.
app.router.add_get('/{rest:.*}', RootView)

app['connected_clients'] = []

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# http://aiohttp.readthedocs.io/en/stable/web.html#graceful-shutdown
async def on_shutdown(app):
  await queue.put(None)
  for client in app['connected_clients']:
    await client.socket.close(code=WSCloseCode.GOING_AWAY)
app.on_shutdown.append(on_shutdown)

async def setup_postgres_pool():
  app['db'] = await create_engine(get_db_url())
  logger.info("Created PSQL engine")

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  loop = asyncio.get_event_loop()
  loop.run_until_complete(setup_postgres_pool())
  loop.create_task(queue_worker(app))
  web.run_app(app)
