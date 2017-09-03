import asyncio
from aiopg.sa import create_engine
from sqlalchemy.sql import select, func

from models import Post, post_table
from utils import get_db_url
from service import Service


class DatabaseException(Exception):
  pass


class Database(Service):
  MAX_SUBTREE_DEPTH = 100

  def __init__(self, app, db_url=None, loop=None):
    super().__init__(app)
    self.loop = loop or asyncio.get_event_loop()
    self.db_url = db_url or get_db_url()
    self.engine = None

  async def startup(self):
    self.engine = await create_engine(self.db_url)
    return self

  async def shutdown(self):
    pass

  async def insert_post(self, parent_id, content=None, ip_address=None):
    async with self.engine.acquire() as conn:
      res = await conn.execute(
        post_table.insert().values(parent_id=parent_id,
                                   content=content,
                                   ip_address=ip_address)
      )
      return dict(await res.first())

  async def get_subtree(self, parent_id):
    async with self.engine.acquire() as conn:
      res = await conn.execute(
        select(['*']).select_from(
          func.subtree(parent_id, self.MAX_SUBTREE_DEPTH)
        )
      )
      return [dict(row) async for row in res]

  async def get_toplevels(self):
    async with self.engine.acquire() as conn:
      res = await conn.execute(
        post_table.select().where(post_table.c.parent_id == None)
      )
      return [dict(row) async for row in res]
