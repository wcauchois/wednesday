from utils import remove_null_values, anonymize_string, unix_time_seconds

def post(post):
  return remove_null_values({
    'id': post['id'],
    'created': ('created' in post) and unix_time_seconds(post['created']),
    'parent_id': post.get('parent_id'),
    'content': post.get('content'),
    'anonymized_author_identifier': \
      ('ip_address' in post) and anonymize_string(post['ip_address'])
  })