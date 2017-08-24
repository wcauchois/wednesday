import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from utils import unix_time_seconds, remove_null_values

Base = declarative_base()

class Post(Base):
  __tablename__ = "posts"
  id = sa.Column(sa.Integer, primary_key=True)
  created = sa.Column(sa.DateTime,
                      server_default=sa.text("now()"))
  parent_id = sa.Column(sa.Integer,
                        sa.ForeignKey("posts.id"))
  content = sa.Column(sa.Text)
  ip_address = sa.Column(sa.String(128))
  score = sa.Column(sa.Float)

post_table = Post.__table__
