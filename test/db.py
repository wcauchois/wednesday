import asyncio
from aiopg.sa import create_engine
import sqlalchemy as sa

import sys
sys.path.insert(0, 'src/python')
from utils import get_db_url
from models import Post

tbl = Post.__table__


async def test1():
    async with create_engine(get_db_url()) as engine:
        async with engine.acquire() as conn:
            print("connection successful")
            res = await conn.execute(tbl.insert().values(parent_id=1, content="test"))
            row = await res.first()
            print(dict(row))


loop = asyncio.get_event_loop()
loop.run_until_complete(test1())
