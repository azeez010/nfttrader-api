"""empty message

Revision ID: ff41c51395b6
Revises: 0f6c21c0ec6a
Create Date: 2022-07-26 12:54:33.167295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff41c51395b6'
down_revision = '0f6c21c0ec6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('name', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('image', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'image')
    op.drop_column('users', 'name')
    # ### end Alembic commands ###
