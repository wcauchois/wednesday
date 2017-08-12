import sys
sys.path.insert(0, 'src/python')

import asyncio
from aiopg.sa import create_engine
import sqlalchemy as sa

import yaml
db_conf = yaml.load(open('config.yml'))['database']
db_url = 'postgresql://{user}:{password}@{host}/{dbname}'.format(**db_conf)


async def go():
    async with create_engine(db_url) as engine:
        async with engine.acquire() as conn:
            print("conn successful")

loop = asyncio.get_event_loop()
loop.run_until_complete(go())
