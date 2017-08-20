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
    self.sub_id = None

  async def send(self, res_type, **values):
    values['type'] = res_type.value
    await self.socket.send_json(values)
    return values

  def __cmp__(self, other):
    return cmp(self.id, other.id)
