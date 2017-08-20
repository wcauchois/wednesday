import logging
from aiohttp import web

from application import app


logger = logging.getLogger(__name__)

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  web.run_app(app)
