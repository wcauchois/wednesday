import yaml


def get_db_url():
    db_conf = yaml.load(open('config.yml'))['database']
    return 'postgresql://{user}:{password}@{host}/{dbname}'.format(**db_conf)
