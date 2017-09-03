import asyncio
import json
from aiopg import create_pool
from collections import defaultdict
import traceback

from client import ResponseType
from utils import get_db_url
from service import Service, ServiceException


class PubSubException(ServiceException):
  pass


class PubSub(Service):
  def __init__(self, app, db_url=None, channel_prefix="pubsub_", loop=None):
    super().__init__(app)
    self.loop = loop or asyncio.get_event_loop()
    self.db_url = db_url or get_db_url()
    self.engine = None
    self.channel_prefix = channel_prefix
    self.subs = defaultdict(set)
    self.to_listen = asyncio.Queue()
    self.to_unlisten = asyncio.Queue()
    self._conn = None
    self._lock = asyncio.Lock()
    self._futures = []

  async def startup(self):
    self.engine = await create_pool(self.db_url)
    self._futures.append(self.loop.create_task(self.listener()))
    return self

  async def shutdown(self):
    if self._conn:
      await self._conn.notifies.put(None)
    await asyncio.gather(*self._futures)

  async def listen_helper(self, conn):
    while True:
      with self.log_exception():
        channel = await self.to_listen.get()
        if channel is None:
          break
        async with self._lock:
          async with conn.cursor() as cur:
            await cur.execute("LISTEN {}".format(channel))

  async def unlisten_helper(self, conn):
    while True:
      with self.log_exception():
        channel = await self.to_unlisten.get()
        if channel is None:
          break
        async with self._lock:
          async with conn.cursor() as cur:
            await cur.execute("UNLISTEN {}".format(channel))

  async def listener(self):
    async with self.engine.acquire() as conn:
      self._conn = conn
      self._futures.extend([self.loop.create_task(self.listen_helper(conn)),
                            self.loop.create_task(self.unlisten_helper(conn))])
      while True:
        with self.log_exception():
          msg = await conn.notifies.get()
          if msg is None:
            # attempt to close coros gracefully
            await self.to_listen.put(None)
            await self.to_unlisten.put(None)
            break
          else:          
            payload = json.loads(msg.payload)
            await asyncio.gather(*[client.send(ResponseType.SUB_NEW_POST, payload) for client in self.subs[msg.channel]])

  async def subscribe(self, post_id, client):
    if not type(post_id) is int:
      raise PubSubException("invalid post_id: {}".format(post_id))
    channel = self.format_channel_name(post_id)
    if client in self.subs[channel]:
      raise PubSubException("already subscribed to id={}".format(post_id))
    self.subs[channel].add(client)
    client.add_subscription(post_id)
    if len(self.subs[channel]) == 1:
      await self.to_listen.put(channel)

  async def unsubscribe(self, post_id, client):
    if not type(post_id) is int:
      raise PubSubException("invalid post_id: {}".format(post_id))
    channel = self.format_channel_name(post_id)
    if client not in self.subs[channel]:
      raise PubSubException("not subscribed to id={}".format(post_id))
    self.subs[channel].remove(client)
    client.remove_subscription(post_id)
    if len(self.subs[channel]) == 0:
      await self.to_unlisten.put(channel)

  async def unsubscribe_all(self, client):
    await asyncio.gather(*[self.unsubscribe(post_id, client) for post_id in client.subscriptions()])

  def format_channel_name(self, post_id):
    return self.channel_prefix + str(post_id)

  async def print_debug_info(self, file):
    print('PubSub(channel_prefix={}):'.format(self.channel_prefix), file=file)
    print('  Subscriptions:', file=file)
    for (key, value) in self.subs.items():
      print('    {}: {}'.format(key, [v.id for v in value]), file=file)
