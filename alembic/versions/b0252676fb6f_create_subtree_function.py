"""create subtree function

Revision ID: b0252676fb6f
Revises: 53c5acb3b17f
Create Date: 2017-08-15 07:41:07.096585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0252676fb6f'
down_revision = '53c5acb3b17f'
branch_labels = None
depends_on = None


def upgrade():
    with open('src/sql/subtree_create.sql') as f:
      op.execute(f.read())


def downgrade():
    with open('src/sql/subtree_drop.sql') as f:
      op.execute(f.read())
