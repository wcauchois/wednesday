import yaml
import datetime

epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_seconds(dt):
  return int((dt - epoch).total_seconds())

def get_db_url():
  db_conf = yaml.load(open('config.yml'))['database']
  return 'postgresql://{user}:{password}@{host}/{dbname}'.format(**db_conf)

def remove_null_values(d):
  ret = dict(d)
  for (key, value) in d.items():
    if ret[key] is None:
      del ret[key]
  return ret
