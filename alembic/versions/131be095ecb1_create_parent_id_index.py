"""create parent_id index

Revision ID: 131be095ecb1
Revises: 59993fa41bea
Create Date: 2017-08-24 11:16:18.110574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '131be095ecb1'
down_revision = '59993fa41bea'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE INDEX posts_parent_id_idx ON posts(parent_id)')


def downgrade():
    op.execute('DROP INDEX posts_parent_id_idx')
