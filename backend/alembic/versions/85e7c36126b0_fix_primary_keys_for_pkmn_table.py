"""fix primary keys for pkmn_table

Revision ID: 85e7c36126b0
Revises: 94b714833797
Create Date: 2026-03-03 03:28:49.403460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85e7c36126b0'
down_revision: Union[str, None] = '94b714833797'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1) Add id column (nullable for now)
    op.add_column("pokemon", sa.Column("id", sa.Integer(), nullable=True))

    # 2) Create a sequence for pokemon.id
    op.execute(sa.text("CREATE SEQUENCE IF NOT EXISTS pokemon_id_seq"))

    # 3) Backfill id for existing rows
    op.execute(sa.text("UPDATE pokemon SET id = nextval('pokemon_id_seq') WHERE id IS NULL"))

    # 4) Set DEFAULT and NOT NULL for id
    op.execute(sa.text("ALTER TABLE pokemon ALTER COLUMN id SET DEFAULT nextval('pokemon_id_seq')"))
    op.alter_column("pokemon", "id", existing_type=sa.Integer(), nullable=False)

    # 5) Drop the old primary key constraint (name might be unknown)
    #    Find it from pg_constraint and drop it dynamically.
    op.execute(
        sa.text(
            """
            DO $$
            DECLARE pk_name text;
            BEGIN
                SELECT c.conname INTO pk_name
                FROM pg_constraint c
                JOIN pg_class t ON t.oid = c.conrelid
                JOIN pg_namespace n ON n.oid = t.relnamespace
                WHERE c.contype = 'p'
                  AND t.relname = 'pokemon'
                  AND n.nspname = current_schema();

                IF pk_name IS NOT NULL THEN
                    EXECUTE format('ALTER TABLE %I.%I DROP CONSTRAINT %I', current_schema(), 'pokemon', pk_name);
                END IF;
            END $$;
            """
        )
    )

    # 6) Create new PK on id
    op.create_primary_key("pk_pokemon_id", "pokemon", ["id"])

    # 7) Ensure unique constraint on (dex_no, forme) exists
    #    Your original migration already added this, but guard just in case.
    op.execute(
        sa.text(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM pg_constraint c
                    JOIN pg_class t ON t.oid = c.conrelid
                    JOIN pg_namespace n ON n.oid = t.relnamespace
                    WHERE c.contype = 'u'
                      AND c.conname = 'uq_pokemon_dex_no_forme'
                      AND t.relname = 'pokemon'
                      AND n.nspname = current_schema()
                ) THEN
                    EXECUTE 'ALTER TABLE pokemon ADD CONSTRAINT uq_pokemon_dex_no_forme UNIQUE (dex_no, forme)';
                END IF;
            END $$;
            """
        )
    )

    # 8) Tie the sequence ownership to pokemon.id (nice to have for cleanup)
    op.execute(sa.text("ALTER SEQUENCE pokemon_id_seq OWNED BY pokemon.id"))


def downgrade() -> None:
    # 1) Drop PK on id
    op.drop_constraint("pk_pokemon_id", "pokemon", type_="primary")

    # 2) Recreate PK on dex_no (name doesn't matter)
    op.create_primary_key(None, "pokemon", ["dex_no"])

    # 3) Drop default and column id
    op.execute(sa.text("ALTER TABLE pokemon ALTER COLUMN id DROP DEFAULT"))
    op.drop_column("pokemon", "id")

    # 4) Drop the sequence
    op.execute(sa.text("DROP SEQUENCE IF EXISTS pokemon_id_seq"))