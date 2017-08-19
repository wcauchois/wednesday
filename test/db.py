import asyncio
from aiopg.sa import create_engine
import sqlalchemy as sa
from sqlalchemy.sql import select, func
from pprint import pprint

import sys
sys.path.insert(0, 'src/python')
from utils import get_db_url
from models import Post, post_table


async def make_data():
  async with create_engine(get_db_url()) as e:
    async with e.acquire() as conn:
      for i in range(10):
        parent_id = 0
        for j in range(10):
          res = await conn.execute(post_table.insert().values(parent_id=parent_id))
          row = await res.first()
          parent_id = row.id

async def test_subtree():
  async with create_engine(get_db_url()) as e:
    async with e.acquire() as conn:
      res = await conn.execute(select(['*']).select_from(func.subtree(0, 5)))
      pprint([dict(row) async for row in res])

loop = asyncio.get_event_loop()
loop.run_until_complete(test_subtree())
