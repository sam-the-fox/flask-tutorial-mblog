"""add users

Revision ID: 3b962ecb72ad
Revises:
Create Date: 2026-11-18 10:47:20.137464

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3b962ecb72ad"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.Text(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_users_email"), ["email"], unique=True)
        batch_op.create_index(
            batch_op.f("ix_users_username"), ["username"], unique=True
        )


def downgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_users_username"))
        batch_op.drop_index(batch_op.f("ix_users_email"))

    op.drop_table("users")
