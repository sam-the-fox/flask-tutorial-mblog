"""add followers

Revision ID: 031f8efba805
Revises: 3ffee8eb82b2
Create Date: 2026-11-20 11:36:02.617805

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "031f8efba805"
down_revision = "3ffee8eb82b2"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "followers",
        sa.Column("follower_id", sa.Integer(), nullable=False),
        sa.Column("followed_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["followed_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["follower_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("follower_id", "followed_id"),
    )


def downgrade():
    op.drop_table("followers")
