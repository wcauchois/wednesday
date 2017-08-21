import asyncio
import logging
from aiohttp import web

from application import app

# can get from config
DEBUG = True


if __name__ == '__main__':
  if DEBUG:
    #loop = asyncio.get_event_loop()
    #loop.set_debug(enabled=True)
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)
  web.run_app(app)
