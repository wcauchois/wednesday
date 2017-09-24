"""alternate scoring algo, improved insert trigger

Revision ID: bf23d105501f
Revises: 1c9f43434bad
Create Date: 2017-09-24 08:50:06.786481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf23d105501f'
down_revision = '1c9f43434bad'
branch_labels = None
depends_on = None


def upgrade():
  with open('src/sql/post_score2_function_create.sql') as f:
    op.execute(f.read())
  with open('src/sql/score_trigger_helper_create.sql') as f:
    op.execute(f.read())
  with open('src/sql/score_trigger_alter_v1.sql') as f:
    op.execute(f.read())


def downgrade():
  with open('src/sql/score_trigger_create.sql') as f:
    op.execute(f.read())
  with open('src/sql/score_trigger_helper_drop.sql') as f:
    op.execute(f.read())
  with open('src/sql/post_score2_function_drop.sql') as f:
    op.execute(f.read())
