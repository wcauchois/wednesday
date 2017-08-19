import asyncio
from aiopg.sa import create_engine
from sqlalchemy.sql import select, func

from utils import get_db_url


class Database:
  MAX_SUBTREE_DEPTH = 100

  def __init__(self):
    self.url = get_db_url()
    self.engine = None
    self.tree = None

  async def setup(self, loop=None):
    if loop is None:
      loop = asyncio.get_event_loop()
    self.engine = await create_engine(self.url)
    return self

  async def get_subtree(self, parent_id):
    with self.engine.acquire() as conn:
      res = await conn.execute(
        select(['*']).select_from(
          func.subtree(parent_id, self.MAX_SUBTREE_DEPTH)
        )
      )
      return [dict(row) async for row in res]
