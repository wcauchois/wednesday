from contextlib import contextmanager
import traceback


class ServiceException(Exception):
  pass


class Service:
  def __init__(self, app):
    self.app = app

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
      self.app.logger.error("got exception!")
      traceback.print_exc() 
