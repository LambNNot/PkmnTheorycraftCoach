"""add abilities to pkmntable

Revision ID: 94b714833797
Revises: 094609ce953d
Create Date: 2026-03-03 03:20:27.101367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94b714833797'
down_revision: Union[str, None] = '094609ce953d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "pokemon",
        "ability_two_id",
        existing_type=sa.Integer(),
        nullable=True,
    )

    op.add_column(
        "pokemon",
        sa.Column("ability_hidden_id", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("pokemon", "ability_hidden_id")

    op.execute(
        sa.text(
            """
            UPDATE pokemon
            SET ability_two_id = ability_one_id
            WHERE ability_two_id IS NULL
            """
        )
    )

    op.alter_column(
        "pokemon",
        "ability_two_id",
        existing_type=sa.Integer(),
        nullable=False,
    )