class Service:
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