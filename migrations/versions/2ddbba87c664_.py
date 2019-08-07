"""empty message

Revision ID: 2ddbba87c664
Revises: cb19f28f6ea2
Create Date: 2019-08-07 16:45:37.099791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ddbba87c664'
down_revision = 'cb19f28f6ea2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('station', sa.Column('numberaddress', sa.String(length=10), nullable=False))
    op.create_unique_constraint(None, 'station', ['numberaddress'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'station', type_='unique')
    op.drop_column('station', 'numberaddress')
    # ### end Alembic commands ###
