from aiohttp import WSCloseCode
from enum import Enum

from utils import get_uuid


# NOTE(amstocker): stuff like this should prob eventually be replaced
#                  by something like protobuf
class ResponseType(Enum):
  TEST          = 'test'
  RPC_SUCCESS   = 'rpc_success'
  RPC_ERROR     = 'rpc_error'
  SYNC_GRAPH    = 'sync_graph'
  UPDATE_GRAPH  = 'update_graph'


class ConnectedClient:
  def __init__(self, socket):
    self.id = get_uuid()
    self.socket = socket
    self.ip_address = None
    self.sub_id = None

  async def send(self, res_type, response):
    response['type'] = res_type.value
    await self.socket.send_json(response)
    return response

  async def close(self):
    await self.socket.close(code=WSCloseCode.GOING_AWAY)

  def __cmp__(self, other):
    return cmp(self.id, other.id)

  def __repr__(self):
    return 'Client(id={}, ip_address={}, sub_id={})'.format(self.id, self.ip_address, self.sub_id)
