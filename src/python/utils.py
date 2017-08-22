import yaml
import hashlib
import uuid
from base64 import b64encode


def unix_time_seconds(dt):
  return int(dt.timestamp())

def get_uuid():
  return uuid.uuid1()

def anonymize_string(s, nchars=8):
  m = hashlib.md5()
  m.update(s.encode('utf-8'))
  return b64encode(m.digest()).decode('utf-8')[:nchars]

def get_ip_address_from_request(req):
  # https://distinctplace.com/2014/04/23/story-behind-x-forwarded-for-and-x-real-ip-headers/
  if 'x-real-ip' in req.headers:
    return req.headers['x-real-ip']
  else:
    # https://github.com/aio-libs/aiohttp/issues/642#issuecomment-158888961
    peername = req.transport.get_extra_info('peername')
    return peername and peername[0] # Host is the first elem of the tuple.

def get_db_url():
  db_conf = yaml.load(open('config.yml'))['database']
  return 'postgresql://{user}:{password}@{host}/{dbname}'.format(**db_conf)

def remove_null_values(d):
  ret = dict(d)
  for (key, value) in d.items():
    if ret[key] is None or ret[key] is False:
      del ret[key]
  return ret
