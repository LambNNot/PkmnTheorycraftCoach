"""userpokeset table

Revision ID: 7632d1170089
Revises: def2ec23be4a
Create Date: 2026-04-20 18:57:43.411829

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7632d1170089'
down_revision: Union[str, None] = 'def2ec23be4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.create_table(
        "user_pokeset",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("pokeset_id", sa.Integer(), nullable=False),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name="fk_user_pokeset_user",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["pokeset_id"],
            ["pokeset.id"],
            name="fk_user_pokeset_pokeset",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_user_pokeset"),
    )

    op.create_index("ix_user_pokeset_user_id", "user_pokeset", ["user_id"])
    op.create_index("ix_user_pokeset_pokeset_id", "user_pokeset", ["pokeset_id"])


def downgrade() -> None:
    op.drop_index("ix_user_pokeset_pokeset_id", table_name="user_pokeset")
    op.drop_index("ix_user_pokeset_user_id", table_name="user_pokeset")
    op.drop_table("user_pokeset")
