import asyncio
from aiopg.sa import create_engine
from sqlalchemy.sql import select, func

from models import Post, post_table
from utils import get_db_url
from service import Service, ServiceException


class DatabaseException(ServiceException):
  pass


class Database(Service):
  MAX_SUBTREE_DEPTH = 1000

  def __init__(self, app, db_url=None, loop=None):
    super().__init__(app, loop=loop)
    self.db_url = db_url or get_db_url()
    self.engine = None

  async def startup(self):
    await super().startup()
    self.engine = await create_engine(self.db_url)

  async def shutdown(self):
    await super().shutdown()

  async def execute(self, query):
    async with self.engine.acquire() as conn:
      return (await conn.execute(query))

  async def execute_one(self, query):
    return dict(await (await self.execute(query)).first())
  
  async def execute_many(self, query):
    return [dict(row) async for row in (await self.execute(query))]

  async def insert_post(self, parent_id, content=None, ip_address=None):
    return (await self.execute_one(
      post_table.insert().values(parent_id=parent_id,
                                 content=content,
                                 ip_address=ip_address)
    ))

  async def get_subtree(self, parent_id):
    return (await self.execute_many(
      select(['*']).select_from(func.subtree(parent_id, self.MAX_SUBTREE_DEPTH))
    ))

  async def get_toplevels(self):
    return (await self.execute_many(
      post_table.select().where(post_table.c.parent_id == None)
    ))
