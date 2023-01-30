"""Create version column

Revision ID: 56a93d0f1be8
Revises: 502e63a83221
Create Date: 2022-11-30 13:20:11.355314

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "56a93d0f1be8"
down_revision = "502e63a83221"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("apm_parameter_file", sa.Column("version", sa.Integer(), nullable=False))
    op.add_column("logfile", sa.Column("version", sa.Integer(), nullable=False))
    op.add_column("telemetry_file", sa.Column("version", sa.Integer(), nullable=False))
    op.add_column("rosbag_file", sa.Column("version", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("rosbag_file", "version")
    op.drop_column("telemetry_file", "version")
    op.drop_column("logfile", "version")
    op.drop_column("apm_parameter_file", "version")
    # ### end Alembic commands ###
