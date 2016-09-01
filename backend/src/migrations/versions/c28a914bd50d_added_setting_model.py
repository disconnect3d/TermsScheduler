"""Added Setting model

Revision ID: c28a914bd50d
Revises: 8e49c4425462
Create Date: 2016-08-31 23:30:57.629196

"""

# revision identifiers, used by Alembic.
revision = 'c28a914bd50d'
down_revision = '8e49c4425462'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('settings',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('name', 'value')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('settings')
    ### end Alembic commands ###