"""alter time scale of post_score2, remove uneccessary var decl

Revision ID: b7086e621748
Revises: bf23d105501f
Create Date: 2017-09-24 09:26:50.550636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7086e621748'
down_revision = 'bf23d105501f'
branch_labels = None
depends_on = None


def upgrade():
  with open('src/sql/post_score2_function_alter_v1.sql') as f:
    op.execute(f.read())
  with open('src/sql/score_trigger_helper_alter_v1.sql') as f:
    op.execute(f.read())


def downgrade():
  with open('src/sql/score_trigger_helper_create.sql') as f:
    op.execute(f.read())
  with open('src/sql/post_score2_function_create.sql') as f:
    op.execute(f.read())
