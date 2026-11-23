"""add posts

Revision ID: 7a5277be2343
Revises: 3b962ecb72ad
Create Date: 2026-11-18 10:54:21.858068

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7a5277be2343"
down_revision = "3b962ecb72ad"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("posts", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_posts_author_id"), ["author_id"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_posts_timestamp"), ["timestamp"], unique=False
        )


def downgrade():
    with op.batch_alter_table("posts", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_posts_timestamp"))
        batch_op.drop_index(batch_op.f("ix_posts_author_id"))

    op.drop_table("posts")
