"""poketeams table

Revision ID: 3b4d577f227f
Revises: 7632d1170089
Create Date: 2026-05-04 12:48:00.829726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b4d577f227f'
down_revision: Union[str, None] = '7632d1170089'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "poke_team",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("authorId", sa.Integer(), nullable=False),

        sa.Column("set1ID", sa.Integer(), nullable=True),
        sa.Column("set2ID", sa.Integer(), nullable=True),
        sa.Column("set3ID", sa.Integer(), nullable=True),
        sa.Column("set4ID", sa.Integer(), nullable=True),
        sa.Column("set5ID", sa.Integer(), nullable=True),
        sa.Column("set6ID", sa.Integer(), nullable=True),

        sa.ForeignKeyConstraint(["authorId"], ["user.id"]),
        sa.ForeignKeyConstraint(["set1ID"], ["pokeset.id"]),
        sa.ForeignKeyConstraint(["set2ID"], ["pokeset.id"]),
        sa.ForeignKeyConstraint(["set3ID"], ["pokeset.id"]),
        sa.ForeignKeyConstraint(["set4ID"], ["pokeset.id"]),
        sa.ForeignKeyConstraint(["set5ID"], ["pokeset.id"]),
        sa.ForeignKeyConstraint(["set6ID"], ["pokeset.id"]),
    )

    op.create_index("ix_poke_team_authorId", "poke_team", ["authorId"])


def downgrade() -> None:
    op.drop_index("ix_poke_team_authorId", table_name="poke_team")
    op.drop_table("poke_team")
