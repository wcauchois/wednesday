"""score update trigger on insert

Revision ID: 1c9f43434bad
Revises: c79c035c5d24
Create Date: 2017-09-23 21:42:36.025764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c9f43434bad'
down_revision = 'c79c035c5d24'
branch_labels = None
depends_on = None


def upgrade():
  with open('src/sql/post_score_function_create.sql') as f:
    op.execute(f.read())
  with open('src/sql/score_trigger_create.sql') as f:
    op.execute(f.read())


def downgrade():
  with open('src/sql/score_trigger_drop.sql') as f:
    op.execute(f.read())
  with open('src/sql/post_score_function_drop.sql') as f:
    op.execute(f.read())
