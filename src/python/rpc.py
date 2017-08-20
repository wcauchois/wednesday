from models import Post, post_table
from client import ConnectedClient, ResponseType


class RpcException(Exception):
  pass


class RpcMethods:
  """
  Each RPC method must be a `@staticmethod` accepting as arguments:
    app: `aiohttp.web.Application`
    client: `client.ConnectedClient`
    args: `list`
  """
  @staticmethod
  async def test(app, client, args):
    ret = {'hello': 'world'}
    if len(args) > 0:
      ret['args'] = args
    return ret

  @staticmethod
  async def will_always_throw(app, client, args):
    raise RpcException('This is an exception!')

  @staticmethod
  async def add_post(app, client, args):
    param = args[0]
    values = {
      'parent_id': param.get('parent_id'),
      'content': param.get('content'),
      'ip_address': get_ip_address_from_request(ws.request)
    }
    res = await app['db'].insert_post(**values)
    return res

  @staticmethod
  async def subscribe(app, client, args):
    post_id = args[0].get('id')
    if client.sub_id:
      await app['ps'].unsubscribe(client, post_id)
    await app['ps'].subscribe(client, post_id)

  @staticmethod
  async def unsubscribe(app, client, args):
    post_id = args[0].get('id')
    await app['ps'].unsubscribe(client, post_id)
