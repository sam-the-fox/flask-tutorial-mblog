"""new fields for users

Revision ID: 3ffee8eb82b2
Revises: 7a5277be2343
Create Date: 2026-11-20 11:12:32.690804

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3ffee8eb82b2"
down_revision = "7a5277be2343"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("about_me", sa.String(length=140), nullable=True))
        batch_op.add_column(sa.Column("last_seen", sa.DateTime(), nullable=True))


def downgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("last_seen")
        batch_op.drop_column("about_me")
