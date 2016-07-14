"""Add Group model & user<->group m2m

Revision ID: 52e5e11c5274
Revises: 4e01db8493bf
Create Date: 2016-07-14 15:00:40.893285

"""

# revision identifiers, used by Alembic.
revision = '52e5e11c5274'
down_revision = '4e01db8493bf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_groups_name'), 'groups', ['name'], unique=True)
    op.create_table('users_groups',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'group_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_groups')
    op.drop_index(op.f('ix_groups_name'), table_name='groups')
    op.drop_table('groups')
    ### end Alembic commands ###
