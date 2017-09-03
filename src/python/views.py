import sys
import asyncio
import json
import logging
from aiohttp import web, WSMsgType, WSCloseCode
from io import StringIO
import aiohttp_jinja2
import traceback

from client import BasicClient, AuthenticatedClient, ResponseType
from rpc import RpcMethods, RpcException
from utils import get_ip_address_from_request, log_short
import application


class RootView(web.View):
  @aiohttp_jinja2.template('index.html')
  async def get(self):
    return {} # Template params


class DebugView(web.View):
  async def get(self):
    app = self.request.app
    with StringIO() as file:
      print('Clients:', file=file)
      for client in app['clients']:
        print('  {}'.format(client), file=file)
      for service in application.services.values():
        await service.print_debug_info(file)
      return web.Response(text=file.getvalue())


class WebSocketView(web.View):
  async def handle_rpc_call(self, payload):
    method_name = payload['method']
    arguments = payload.get('arguments', [])
    response = {'call_id' : payload['call_id']}
    res_type = ResponseType.RPC_ERROR
    try:
      func = getattr(RpcMethods, method_name)
    except AttributeError:
      response['message'] = 'Unknown method: {}'.format(method_name)
    else:
      try:
        ret = await func(self.request.app, self, arguments)
      except RpcException as e:
        response['message'] = str(e)
        traceback.print_exc()
      except:
        response['message'] = 'SERVER ERROR'
        traceback.print_exc()
      else:
        response['return_value'] = json.dumps(ret)
        res_type = ResponseType.RPC_SUCCESS
    finally:
      return (await self.client.send(res_type, response))

  async def get(self):
    self.logger = self.request.app.logger
    self.websocket = web.WebSocketResponse()
    self.client = BasicClient(self.websocket)
    await self.websocket.prepare(self.request)
    self.logger.info('WebSocket client connected')
    async for msg in self.websocket:
      if msg.type == WSMsgType.TEXT:
        self.logger.info('Got WebSocket data: {}'.format(log_short(msg.data)))
        payload = json.loads(msg.data)
        if payload['type'] == 'rpc':
          response = await self.handle_rpc_call(payload)
          self.logger.info('Sending WebSocket data: {}'.format(log_short(response)))
      elif msg.type == WSMsgType.ERROR:
        self.logger.error('WebSocket error: {}'.format(self.websocket.exception()))
    else:
      self.logger.info('WebSocket connection closed')
      if self.client.authenticated:
        await self.request.app['ps'].unsubscribe_all(self.client)
        del self.request.app['clients'][self.client.id]
    return self.websocket
