from aiohttp import WSCloseCode
from enum import Enum

from utils import get_uuid


# NOTE(amstocker): stuff like this should prob eventually be replaced
#                  by something like protobuf
class ResponseType(Enum):
  TEST          = 'test'
  RPC_SUCCESS   = 'rpc_success'
  RPC_ERROR     = 'rpc_error'
  SUB_NEW_POST  = 'sub_new_post'


class BasicClient:
  def __init__(self, socket, id=None):
    self.id = id or get_uuid()
    self.socket = socket
    self.ip_address = None
    self.subbed_ids = set()
    self.authenticated = False

  async def send(self, res_type, response):
    response['type'] = res_type.value
    await self.socket.send_json(response)
    return response

  async def close(self):
    await self.socket.close(code=WSCloseCode.GOING_AWAY)

  def subscriptions(self):
    return self.subbed_ids

  def add_subscription(self, post_id):
    self.subbed_ids.add(post_id)

  def remove_subscription(self, post_id):
    if post_id in self.subbed_ids:
      self.subbed_ids.remove(post_id)

  def __cmp__(self, other):
    return cmp(self.id, other.id)

  def __repr__(self):
    return '{}(id={}, ip_address={})' \
      .format(self.__class__.__name__, self.id, self.ip_address)


class AuthenticatedClient(BasicClient):
  def __init__(self, socket, id=None):
    super().__init__(socket, id=id)
    self.authenticated = True
