"""empty message

Revision ID: a98e7552f9cb
Revises: 52264ef2a19c
Create Date: 2022-07-26 16:40:18.681565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a98e7552f9cb'
down_revision = '52264ef2a19c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=32), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('image', sa.String(length=128), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.create_table('nft_trades',
    sa.Column('nft_id', sa.Integer(), nullable=True),
    sa.Column('trades_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['nft_id'], ['nft.id'], ),
    sa.ForeignKeyConstraint(['trades_id'], ['trades.id'], )
    )
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
    op.add_column('nft', sa.Column('owner', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'nft', 'user', ['owner'], ['id'])
    op.add_column('trades', sa.Column('status', sa.Boolean(), nullable=True))
    op.add_column('trades', sa.Column('owner', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'trades', 'user', ['owner'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'trades', type_='foreignkey')
    op.drop_column('trades', 'owner')
    op.drop_column('trades', 'status')
    op.drop_constraint(None, 'nft', type_='foreignkey')
    op.drop_column('nft', 'owner')
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=32), nullable=True),
    sa.Column('admin', sa.BOOLEAN(), nullable=True),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('image', sa.VARCHAR(length=128), nullable=True),
    sa.Column('password', sa.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    op.drop_table('nft_trades')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###