"""Add log file as a separate entity and include tlogfile uri

Revision ID: 9f96a8e16f9e
Revises: 91a66a83d358
Create Date: 2022-08-01 10:52:49.229925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f96a8e16f9e'
down_revision = '91a66a83d358'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logfile',
    sa.Column('file_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('file_uri', sa.String(), nullable=True),
    sa.Column('flight_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['flight_id'], ['flight.flight_id'], ),
    sa.PrimaryKeyConstraint('file_id')
    )
    op.add_column('flight', sa.Column('tfile_uri', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flight', sa.Column('file_uri', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('flight', 'tfile_uri')
    op.drop_table('logfile')
    # ### end Alembic commands ###
