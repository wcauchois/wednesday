"""set parent_id nullable

Revision ID: 52dcffd99d86
Revises: 83ef3fcbf96f
Create Date: 2017-08-12 03:20:30.874324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52dcffd99d86'
down_revision = '83ef3fcbf96f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'parent_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'parent_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###