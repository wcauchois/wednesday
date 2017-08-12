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

  def to_json(self):
    return remove_null_values({
      'id': self.id,
      'created': self.created and unix_time_seconds(self.created),
      'parent_id': self.parent_id,
      'content': self.content
    })

post_table = Post.__table__
