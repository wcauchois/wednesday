import asyncio
import json
from aiopg import create_pool
from collections import defaultdict

from client import ResponseType
from utils import get_db_url


class PubSubException(Exception):
  pass


class PubSub:
  def __init__(self, app, db_url=None, channel_prefix="pubsub_", loop=None):
    self.app = app
    self.loop = loop or asyncio.get_event_loop()
    self.db_url = db_url or get_db_url()
    self.engine = None
    self.channel_prefix = channel_prefix
    self.subs = defaultdict(set)
    self.to_listen = asyncio.Queue()
    self.to_unlisten = asyncio.Queue()
    self._lock = asyncio.Lock()
    self._futures = []

  async def startup(self):
    self.engine = await create_pool(self.db_url)
    self._futures.append(self.loop.create_task(self.listener()))
    return self

  async def shutdown(self):
    [f.cancel() for f in self._futures]

  async def listen_helper(self, conn):
    while True:
      channel = await self.to_listen.get()
      async with self._lock:
        async with conn.cursor() as cur:
          await cur.execute("LISTEN {}".format(channel))

  async def unlisten_helper(self, conn):
    while True:
      channel = await self.to_unlisten.get()
      async with self._lock:
        async with conn.cursor() as cur:
          await cur.execute("UNLISTEN {}".format(channel))

  async def listener(self):
    async with self.engine.acquire() as conn:
      self._futures.extend([self.loop.create_task(self.listen_helper(conn)),
                            self.loop.create_task(self.unlisten_helper(conn))])
      while True:
        msg = await conn.notifies.get()
        payload = json.loads(msg.payload)
        # XXX(amstocker): should use proper response type
        await asyncio.gather(*[client.send(ResponseType.TEST, payload) for client in self.subs[msg.channel]])

  async def subscribe(self, client):
    if client.sub_id is None:
      return
    channel = self.format_channel_name(client.sub_id)
    self.subs[channel].add(client)
    if len(self.subs[channel]) == 1:
      await self.to_listen.put(channel)

  async def unsubscribe(self, client):
    if client.sub_id is None:
      return
    channel = self.format_channel_name(client.sub_id)
    self.subs[channel].remove(client)
    if len(self.subs[channel]) == 0:
      await self.to_unlisten.put(channel)

  def format_channel_name(self, post_id):
    return self.channel_prefix + str(post_id)

  def print_debug_info(self, file):
    print('PubSub(channel_prefix={}):'.format(self.channel_prefix), file=file)
    print('  Subscriptions:', file=file)
    for (key, value) in self.subs.items():
      print('    {}: {}'.format(key, [v.id for v in value]), file=file)
