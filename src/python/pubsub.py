import asyncio
import json
from aiopg import create_pool
from collections import defaultdict

from client import ResponseType
from utils import get_db_url


class PubSubException(Exception):
  pass


class PubSub:
  def __init__(self, db_url=None, channel_prefix="pubsub_", loop=None):
    self.loop = loop or asyncio.get_event_loop()
    self.db_url = db_url or get_db_url()
    self.engine = None
    self.channel_prefix = channel_prefix
    self.subs = defaultdict(set)
    self.running = False
    self.to_listen = asyncio.Queue()
    self.to_unlisten = asyncio.Queue()
    self._futures = []

  async def startup(self):
    self.engine = await create_pool(self.db_url)
    self.running = True
    self._futures.append(self.loop.create_task(self.listener()))
    return self

  async def shutdown(self):
    self.running = False
    [f.cancel() for f in self._futures]

  async def listen_helper(self, cur):
    while self.running:
      post_id = await self.to_listen.get()
      await cur.execute("LISTEN {}".format(self.format_channel_name(post_id)))

  async def unlisten_helper(self, cur):
    while self.running:
      post_id = await self.to_unlisten.get()
      await cur.execute("UNLISTEN {}".format(self.format_channel_name(post_id)))

  async def listener(self):
    async with self.engine.acquire() as conn:
      async with conn.cursor() as cur:
        self._futures.extend([self.loop.create_task(self.listen_helper(cur)),
                              self.loop.create_task(self.unlisten_helper(cur))])
        while self.running:
          msg = await conn.notifies.get()
          payload = json.loads(msg.payload)
          # XXX(amstocker): should use proper response type
          asyncio.gather(*[client.send(ResponseType.TEST, **payload) for client in self.subs[payload['id']]])

  async def subscribe(self, client, post_id):
    self.subs[post_id].add(client)
    if len(self.subs[post_id]) == 1:
      await self.to_listen.put(post_id)

  async def unsubscribe(self, client, post_id):
    self.subs[post_id].remove(client)
    if len(self.subs[post_id]) == 0:
      await self.to_unlisten.put(post_id)

  def format_channel_name(self, post_id):
    return self.channel_prefix + str(post_id)
