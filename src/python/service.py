import asyncio
from contextlib import contextmanager

from utils import log_traceback


class ServiceException(Exception):
  pass


class Service:
  def __init__(self, app, loop=None):
    self.app = app
    self.logger = app.logger
    self.loop = loop or asyncio.get_event_loop()

  @property
  def init_order(self):
    """
    Influences the order in which this service is initialized, compared to other services.
    Lower numbers are initialized first.
    """
    return 99

  async def startup(self):
    pass

  async def shutdown(self):
    pass

  async def print_debug_info(self, file):
    pass

  @contextmanager
  def log_exception(self):
    try:
      yield
    except:
      log_traceback(self.app.logger)

  @staticmethod
  def async_log_exception(async_method):
    async def wrapper(self, *args, **kwargs):
      try:
        return (await async_method(self, *args, **kwargs))
      except:
        self.app.logger.error("{}.{} encountered an exception:".format(
          self.__class__.__name__, async_method.__name__))
        log_traceback(self.app.logger)
    return wrapper
