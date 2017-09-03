"""update subtree function

Revision ID: c79c035c5d24
Revises: 131be095ecb1
Create Date: 2017-09-03 06:08:46.017925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c79c035c5d24'
down_revision = '131be095ecb1'
branch_labels = None
depends_on = None


def upgrade():
    with open('src/sql/subtree_alter_v1.sql') as f:
      op.execute(f.read())


def downgrade():
    # NOTE(amstocker): this is dropped instead of unaltered because
    # the previous revision added a column which made this function
    # cause an error.
    with open('src/sql/subtree_drop.sql') as f:
      op.execute(f.read())
