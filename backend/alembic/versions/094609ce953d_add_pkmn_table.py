"""add pkmn table

Revision ID: 094609ce953d
Revises: 94aa4a754c82
Create Date: 2026-02-03 18:15:33.303860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '094609ce953d'
down_revision: Union[str, None] = '94aa4a754c82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "pokemon",
        sa.Column("dex_no", sa.Integer, nullable=False),
        sa.Column("species", sa.String(length=100), nullable=False),
        sa.Column("type_code", sa.Integer, nullable=False),
        sa.Column("forme", sa.String(length=50), nullable=False),
        sa.Column("ability_one_id", sa.Integer, nullable=False),
        sa.Column("ability_two_id", sa.Integer, nullable=False),
        sa.Column("base_hp", sa.Integer, nullable=False),
        sa.Column("base_atk", sa.Integer, nullable=False),
        sa.Column("base_def", sa.Integer, nullable=False),
        sa.Column("base_spa", sa.Integer, nullable=False),
        sa.Column("base_spd", sa.Integer, nullable=False),
        sa.Column("base_spe", sa.Integer, nullable=False),
        sa.Column("weight", sa.Float, nullable=False),
        sa.PrimaryKeyConstraint("dex_no"),
        sa.UniqueConstraint("dex_no", "forme", name="uq_pokemon_dex_no_forme"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("pokemon")