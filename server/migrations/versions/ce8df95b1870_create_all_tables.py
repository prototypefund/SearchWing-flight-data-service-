"""Create all tables

Revision ID: ce8df95b1870
Revises:
Create Date: 2023-03-01 14:21:46.847789

"""
import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ce8df95b1870"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "mission",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("alias", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("location", sa.String(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column(
            "geo",
            geoalchemy2.types.Geometry(geometry_type="POINT", from_text="ST_GeomFromEWKT", name="geometry"),
            nullable=True,
        ),
        sa.Column("is_test", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("alias"),
    )
    op.create_index(op.f("ix_mission_id"), "mission", ["id"], unique=False)
    op.create_table(
        "plane",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("alias", sa.String(), nullable=False),
        sa.Column("model", sa.String(), nullable=True),
        sa.Column("in_use", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("alias"),
    )
    op.create_index(op.f("ix_plane_id"), "plane", ["id"], unique=False)
    op.create_table(
        "flight",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("plane_id", sa.Integer(), nullable=False),
        sa.Column("mission_id", sa.Integer(), nullable=False),
        sa.Column("average_speed", sa.Float(), nullable=True),
        sa.Column("distance", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column(
            "geo",
            geoalchemy2.types.Geometry(geometry_type="POINT", from_text="ST_GeomFromEWKT", name="geometry"),
            nullable=True,
        ),
        sa.Column("pilot", sa.String(), nullable=True),
        sa.Column("observer", sa.String(), nullable=True),
        sa.Column(
            "weather_conditions",
            sa.Enum("sunny", "windy", "cloudy", "rainy", "snow", name="weathercondititions"),
            nullable=True,
        ),
        sa.Column("temperature", sa.Integer(), nullable=True),
        sa.Column("start_time", sa.DateTime(), nullable=True),
        sa.Column("end_time", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["mission_id"],
            ["mission.id"],
        ),
        sa.ForeignKeyConstraint(
            ["plane_id"],
            ["plane.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_flight_id"), "flight", ["id"], unique=False)
    op.create_table(
        "flight_files",
        sa.Column("file_type", sa.String(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.Column("file_uri", sa.String(), nullable=False),
        sa.Column("flight_id", sa.Integer(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["flight_id"],
            ["flight.id"],
        ),
        sa.PrimaryKeyConstraint("file_uri"),
        sa.UniqueConstraint("file_uri"),
    )
    op.create_table(
        "misssion_flight_association",
        sa.Column("mission_id", sa.Integer(), nullable=False),
        sa.Column("flight_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["flight_id"],
            ["flight.id"],
        ),
        sa.ForeignKeyConstraint(
            ["mission_id"],
            ["mission.id"],
        ),
        sa.PrimaryKeyConstraint("mission_id", "flight_id"),
    )
    op.create_table(
        "plane_mission_association",
        sa.Column("plane_id", sa.Integer(), nullable=False),
        sa.Column("flight_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["flight_id"],
            ["flight.id"],
        ),
        sa.ForeignKeyConstraint(
            ["plane_id"],
            ["plane.id"],
        ),
        sa.PrimaryKeyConstraint("plane_id", "flight_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("plane_mission_association")
    op.drop_table("misssion_flight_association")
    op.drop_table("flight_files")
    op.drop_index(op.f("ix_flight_id"), table_name="flight")
    op.drop_table("flight")
    op.drop_index(op.f("ix_plane_id"), table_name="plane")
    op.drop_table("plane")
    op.drop_index(op.f("ix_mission_id"), table_name="mission")
    op.drop_table("mission")
    # ### end Alembic commands ###
