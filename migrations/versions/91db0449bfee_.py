"""empty message

Revision ID: 91db0449bfee
Revises: 3840cfd9bd23
Create Date: 2022-07-29 18:30:31.075672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91db0449bfee'
down_revision = '3840cfd9bd23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('nonce', sa.String(length=128), nullable=True))
    op.create_unique_constraint(None, 'user', ['account'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'nonce')
    # ### end Alembic commands ###
