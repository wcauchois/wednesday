import asyncio
from aiopg.sa import create_engine
import sqlalchemy as sa

import sys
sys.path.insert(0, 'src/python')
from utils import get_db_url
from models import Post

tbl = Post.__table__


async def test1():
    async with create_engine(get_db_url()) as e:
        async with e.acquire() as conn:
            print("connection successful")
            data = [{"parent_id":1, "content":"test"}]
            print(str(tbl.insert().values(**data[0])))
            res = await conn.execute(tbl.insert().values(**data[0]))
            row = await res.first()
            print(dict(row))
            async for row in conn.execute(tbl.select()):
                print(row.keys())


loop = asyncio.get_event_loop()
loop.run_until_complete(test1())
