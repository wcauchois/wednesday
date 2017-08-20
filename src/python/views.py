import asyncio
import json
from aiohttp import (
  web, WSMsgType, WSCloseCode
)
import aiohttp_jinja2

from client import ConnectedClient, ResponseType
from rpc import RpcMethods, RpcException


class RootView(web.View):
  @aiohttp_jinja2.template('index.html')
  async def get(self):
    return {} # Template params


class WebSocketView(web.View):
  async def handle_rpc_call(self, payload):
    method_name = payload['method']
    call_id = payload['call_id']
    arguments = payload.get('arguments', [])
    func = getattr(RpcMethods, method_name)
    try:
      if func is not None:
        ret = await func(self.request.app, self.client, arguments)
        response = {'return_value': json.dumps(ret)}
        res_type = ResponseType.RPC_SUCCESS
      else:
        raise RpcException('Unknown method: {}'.format(method_name))
    except RpcException as e:
      logging.exception('RPC exception') # Prints traceback
      response = {'message': str(e)}
      res_type = ResponseType.RPC_ERROR
    response['call_id'] = call_id
    return (await self.client.send(res_type, response))

  #async def send_initial_graph_sync(self):
  #  g = await convert_posts_into_graph_store(self.request.app)
  #  self.client.post_graph = g
  #  self.client.socket.send_json({
  #    'type': 'sync_graph',
  #    'graph': g.serialize()
  #  })

  async def get(self):
    ws = web.WebSocketResponse()
    await ws.prepare(self.request)
    logger.info('WebSocket client connected')
    self.client = ConnectedClient(ws)
    self.request.app['clients'].add(self.client)
    # Could get variables from session here for auth etc
    #asyncio.ensure_future(self.send_initial_graph_sync()) # Background
    async for msg in ws:
      if msg.type == WSMsgType.TEXT:
        logger.info('Got WebSocket data: {}'.format(msg.data))
        payload = json.loads(msg.data)
        if payload['type'] == 'rpc':
          response = await self.handle_rpc_call(payload)
          logger.info('Sending WebSocket data: {}'.format(response))
      elif msg.type == WSMsgType.ERROR:
        logger.error('WebSocket error: {}'.format(ws.exception()))
    logger.info('WebSocket connection closed')
    self.request.app['clients'].remove(self.client)
    return ws
