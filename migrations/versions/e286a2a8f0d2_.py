"""empty message

Revision ID: e286a2a8f0d2
Revises: 3d6ba6dd3f74
Create Date: 2019-08-02 23:50:37.807534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e286a2a8f0d2'
down_revision = '3d6ba6dd3f74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('station',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('lattitude', sa.String(length=80), nullable=False),
    sa.Column('longitude', sa.String(length=80), nullable=False),
    sa.Column('responsibleUser', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=120), nullable=True),
    sa.Column('organization', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['organization'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('description'),
    sa.UniqueConstraint('lattitude'),
    sa.UniqueConstraint('longitude'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('station')
    # ### end Alembic commands ###
