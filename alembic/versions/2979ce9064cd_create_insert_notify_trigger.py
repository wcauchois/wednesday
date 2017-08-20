"""create insert notify trigger

Revision ID: 2979ce9064cd
Revises: b0252676fb6f
Create Date: 2017-08-20 07:14:06.887539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2979ce9064cd'
down_revision = 'b0252676fb6f'
branch_labels = None
depends_on = None


def upgrade():
    with open('src/sql/insert_trigger_create.sql') as f:
      op.execute(f.read())


def downgrade():
    with open('src/sql/insert_trigger_drop.sql') as f:
      op.execute(f.read())
