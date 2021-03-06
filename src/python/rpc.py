from functools import wraps

import render
from models import Post, post_table
from client import AuthenticatedClient, ResponseType
from utils import get_ip_address_from_request
from pubsub import PubSubException


class RpcException(Exception):
  pass


def require_authentication(method):
  @wraps(method)
  def wrapper(app, view, args):
    # NOTE(amstocker): in the future this can be more robust
    if view.client.authenticated:
      return method(app, view, args)
    else:
      raise RpcException('Handshake not completed')
  return wrapper

def pass_args0_as_kwargs(method):
  @wraps(method)
  def wrapper(app, view, args):
    if isinstance(args, list) \
        and len(args) > 0 \
        and isinstance(args[0], dict):
      return method(app, view, **args[0])
    else:
      raise RpcException('Invalid arguments (expecting dict for args[0])')
  return wrapper


class RpcMethods:
  """
  Each RPC method must be a `@staticmethod` accepting as arguments:
    app: `aiohttp.web.Application`
    view: `views.WebSocketView`
    args: `list`
  """
  @staticmethod
  async def test(app, view, args):
    ret = {'hello': 'world'}
    if len(args) > 0:
      ret['args'] = args
    return ret

  @staticmethod
  async def will_always_throw(app, view, args):
    raise RpcException('This is an exception!')

  @staticmethod
  @pass_args0_as_kwargs
  async def handshake(app, view, client_id=None):
    if not client_id:
      view.client = AuthenticatedClient(view.websocket)
      view.client.ip_address = get_ip_address_from_request(view.request)
      app['clients'][view.client.id] = view.client
    elif client_id in app['clients']:
      view.client = app['clients'][client_id]
      view.client.socket = view.websocket
    else:
      raise RpcException('Invalid client_id')
    return {'client_id': str(view.client.id)}        

  @staticmethod
  @require_authentication
  @pass_args0_as_kwargs
  async def get_tree(app, view, id=None):
    posts = await app['db'].get_subtree(id)
    return [render.post(p) for p in posts]

  @staticmethod
  @require_authentication
  async def get_toplevels(app, view, args):
    return [render.post(p) for p in (await app['db'].get_toplevels())]

  @staticmethod
  @require_authentication
  @pass_args0_as_kwargs
  async def get_hot(app, view, n=10):
    try:
      n = max(int(n), 0)
    except:
      raise RpcException('Invalid number: {}'.format(n))
    return [render.post(p) for p in (await app['db'].get_hot_all(n))]

  @staticmethod
  @require_authentication
  @pass_args0_as_kwargs
  async def add_post(app, view, parent_id=None, content=None):
    return (await app['db'].insert_post(parent_id=parent_id, content=content,
                                        ip_address=view.client.ip_address))

  @staticmethod
  @require_authentication
  @pass_args0_as_kwargs
  async def subscribe(app, view, id=None):
    await app['ps'].subscribe(id, view.client)
    return {"message": "successfully subscribed to id={}".format(id)}
    
  @staticmethod
  @require_authentication
  @pass_args0_as_kwargs
  async def unsubscribe(app, view, id=None):
    await app['ps'].unsubscribe(id, view.client)
    return {"message": "successfully unsubscribed from id={}".format(id)}
