"""alter post_score2 v2

Revision ID: f4b93159a6b6
Revises: b7086e621748
Create Date: 2017-09-28 20:04:00.579709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4b93159a6b6'
down_revision = 'b7086e621748'
branch_labels = None
depends_on = None


def upgrade():
  with open('src/sql/post_score2_function_alter_v2.sql') as f:
    op.execute(f.read())

def downgrade():
  with open('src/sql/post_score2_function_alter_v1.sql') as f:
    op.execute(f.read())
