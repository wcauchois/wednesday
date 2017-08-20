"""alter insert trigger v1

Revision ID: a38376dcc8ae
Revises: 2979ce9064cd
Create Date: 2017-08-20 17:35:50.974462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a38376dcc8ae'
down_revision = '2979ce9064cd'
branch_labels = None
depends_on = None


def upgrade():
    with open('src/sql/insert_trigger_alter_v1.sql') as f:
      op.execute(f.read())


def downgrade():
    with open('src/sql/insert_trigger_create.sql') as f:
      op.execute(f.read())
