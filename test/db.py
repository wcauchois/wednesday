import asyncio
from aiopg import create_pool
from aiopg.sa import create_engine
import sqlalchemy as sa
from sqlalchemy.sql import select, func
from pprint import pprint

import sys
sys.path.insert(0, 'src/python')
from database import Database
from pubsub import PubSub
from models import Post, post_table
from utils import get_db_url


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

async def listen_helper(conn):
  async with conn.cursor() as cur:
    await cur.execute("LISTEN pubsub_0")
    await cur.execute("LISTEN pubsub_290")
    msg = await conn.notifies.get()
    print('NOTIFY:', msg.payload)
    msg = await conn.notifies.get()
    print('NOTIFY:', msg.payload)

async def test_pubsub():
	async with create_pool(get_db_url()) as e:
		async with e.acquire() as listen_conn:
			listener = listen_helper(listen_conn)
			db = Database()
			await db.startup()
			await asyncio.gather(listener, db.insert_post(parent_id=290, content='testing notify'))
			print("listen/notify done!")

loop = asyncio.get_event_loop()
loop.run_until_complete(test_pubsub())
