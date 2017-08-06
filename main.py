import asyncio
from aiohttp import web
import aiopg
import yaml
import logging

logger = logging.getLogger(__name__)

config = yaml.load(open('config.yml'))
db_conf = config['database']
dsn = 'dbname={} user={} password={} host={}'.format(
  db_conf['dbname'], db_conf['user'], db_conf['password'], db_conf['host'])

def index():
  return """\
<!DOCTYPE html>
<html>
  <head>
    <title>It's Wednesday, my dudes</title>
  </head>
  <body>
    <div id="container"></div>
    <script type="text/javascript" src="dist/bundle.js"></script>
  </body>
</html>
"""

async def handle(request):
  async with pool.acquire() as conn:
    async with conn.cursor() as cur:
      await cur.execute('select * from posts')
      ret = []
      async for row in cur:
        ret.append(row)
      return web.Response(text=index(), content_type='text/html')
      #return web.Response(text='got from db: {}'.format(ret))
  #name = request.match_info.get('name', "Anonymous")
  #text = "Hello, " + name
  #return web.Response(text=text)

async def setup_postgres_pool():
  global pool
  pool = await aiopg.create_pool(dsn)
  logger.info("Created PSQL pool")

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)
app.router.add_static('/dist', './dist')

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  loop = asyncio.get_event_loop()
  loop.run_until_complete(setup_postgres_pool())
  web.run_app(app)

