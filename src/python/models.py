import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    id = sa.Column(sa.Integer, primary_key=True)
    created = sa.Column(sa.DateTime,
                        server_default=sa.text("now()"))
    parent_id = sa.Column(sa.Integer,
                        sa.ForeignKey("posts.id"),
                        nullable=False)
    content = sa.Column(sa.Text)
