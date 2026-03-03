"""add other core tables

Revision ID: 5067c20abaa9
Revises: 85e7c36126b0
Create Date: 2026-03-03 03:43:01.830070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5067c20abaa9'
down_revision: Union[str, None] = '85e7c36126b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # --- ability ---
    op.create_table(
        "ability",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=2000), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_ability"),
        sa.UniqueConstraint("name", name="uq_ability_name"),
    )

    # --- item ---
    op.create_table(
        "item",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=2000), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_item"),
        sa.UniqueConstraint("name", name="uq_item_name"),
    )

    # --- type ---
    op.create_table(
        "type",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type_code", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=2000), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_type"),
        sa.UniqueConstraint("type_code", name="uq_type_type_code"),
        sa.UniqueConstraint("name", name="uq_type_name"),
    )

    # --- nature ---
    op.create_table(
        "nature",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("hp", sa.Float(), nullable=False),
        sa.Column("atk", sa.Float(), nullable=False),
        sa.Column("dfn", sa.Float(), nullable=False),
        sa.Column("spa", sa.Float(), nullable=False),
        sa.Column("spd", sa.Float(), nullable=False),
        sa.Column("spe", sa.Float(), nullable=False),
        sa.Column("summary", sa.String(length=500), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_nature"),
        sa.UniqueConstraint("name", name="uq_nature_name"),
    )

    # --- user ---
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_user"),
        sa.UniqueConstraint("username", name="uq_user_username"),
    )

    # --- type_effectiveness (composite PK) ---
    op.create_table(
        "type_effectiveness",
        sa.Column("attack_type_id", sa.Integer(), nullable=False),
        sa.Column("defense_type_id", sa.Integer(), nullable=False),
        sa.Column("multiplier", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("attack_type_id", "defense_type_id", name="pk_type_effectiveness"),
        sa.ForeignKeyConstraint(
            ["attack_type_id"],
            ["type.id"],
            name="fk_type_eff_attack",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["defense_type_id"],
            ["type.id"],
            name="fk_type_eff_defense",
            ondelete="CASCADE",
        ),
    )

    # Indexes for effectiveness lookups
    op.create_index("ix_type_eff_attack_type_id", "type_effectiveness", ["attack_type_id"])
    op.create_index("ix_type_eff_defense_type_id", "type_effectiveness", ["defense_type_id"])

    # --- pokeset ---
    op.create_table(
        "pokeset",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("mon_id", sa.Integer(), nullable=False),        # -> pokemon.id
        sa.Column("item_id", sa.Integer(), nullable=True),        # optional
        sa.Column("ability_id", sa.Integer(), nullable=False),    # -> ability.id
        sa.Column("nature_id", sa.Integer(), nullable=False),     # -> nature.id

        sa.Column("hp_ev", sa.Integer(), nullable=False),
        sa.Column("atk_ev", sa.Integer(), nullable=False),
        sa.Column("def_ev", sa.Integer(), nullable=False),
        sa.Column("spa_ev", sa.Integer(), nullable=False),
        sa.Column("spd_ev", sa.Integer(), nullable=False),
        sa.Column("spe_ev", sa.Integer(), nullable=False),

        sa.Column("hp_iv", sa.Integer(), nullable=False),
        sa.Column("atk_iv", sa.Integer(), nullable=False),
        sa.Column("def_iv", sa.Integer(), nullable=False),
        sa.Column("spa_iv", sa.Integer(), nullable=False),
        sa.Column("spd_iv", sa.Integer(), nullable=False),
        sa.Column("spe_iv", sa.Integer(), nullable=False),

        sa.PrimaryKeyConstraint("id", name="pk_pokeset"),

        sa.ForeignKeyConstraint(
            ["mon_id"],
            ["pokemon.id"],
            name="fk_pokeset_mon",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["item_id"],
            ["item.id"],
            name="fk_pokeset_item",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["ability_id"],
            ["ability.id"],
            name="fk_pokeset_ability",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["nature_id"],
            ["nature.id"],
            name="fk_pokeset_nature",
            ondelete="RESTRICT",
        ),
    )

    op.create_index("ix_pokeset_mon_id", "pokeset", ["mon_id"])
    op.create_index("ix_pokeset_item_id", "pokeset", ["item_id"])
    op.create_index("ix_pokeset_ability_id", "pokeset", ["ability_id"])
    op.create_index("ix_pokeset_nature_id", "pokeset", ["nature_id"])

    # --- add foreign keys to pokemon ability columns ---
    # pokemon table already exists (created in earlier migration), so we add constraints here.
    with op.batch_alter_table("pokemon") as batch_op:
        batch_op.create_foreign_key(
            "fk_pokemon_ability_one",
            "ability",
            ["ability_one_id"],
            ["id"],
            ondelete="RESTRICT",
        )
        batch_op.create_foreign_key(
            "fk_pokemon_ability_two",
            "ability",
            ["ability_two_id"],
            ["id"],
            ondelete="SET NULL",
        )
        batch_op.create_foreign_key(
            "fk_pokemon_ability_hidden",
            "ability",
            ["ability_hidden_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    # --- drop pokemon foreign keys ---
    with op.batch_alter_table("pokemon") as batch_op:
        batch_op.drop_constraint("fk_pokemon_ability_hidden", type_="foreignkey")
        batch_op.drop_constraint("fk_pokemon_ability_two", type_="foreignkey")
        batch_op.drop_constraint("fk_pokemon_ability_one", type_="foreignkey")

    # --- drop pokeset and its indexes ---
    op.drop_index("ix_pokeset_nature_id", table_name="pokeset")
    op.drop_index("ix_pokeset_ability_id", table_name="pokeset")
    op.drop_index("ix_pokeset_item_id", table_name="pokeset")
    op.drop_index("ix_pokeset_mon_id", table_name="pokeset")
    op.drop_table("pokeset")

    # --- drop type_effectiveness and its indexes ---
    op.drop_index("ix_type_eff_defense_type_id", table_name="type_effectiveness")
    op.drop_index("ix_type_eff_attack_type_id", table_name="type_effectiveness")
    op.drop_table("type_effectiveness")

    # --- drop remaining tables (reverse dependency order) ---
    op.drop_table("user")
    op.drop_table("nature")
    op.drop_table("type")
    op.drop_table("item")
    op.drop_table("ability")