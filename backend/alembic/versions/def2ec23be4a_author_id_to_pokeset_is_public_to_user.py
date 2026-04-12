"""author_id to PokeSet; is_public to User

Revision ID: def2ec23be4a
Revises: 5067c20abaa9
Create Date: 2026-03-03 18:18:39.667531

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'def2ec23be4a'
down_revision: Union[str, None] = '5067c20abaa9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # --- user: add is_public (boolean) ---
    # Backfill existing rows with TRUE by default, then remove the default if you want explicit writes.
    op.add_column(
        "user",
        sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )
    op.alter_column("user", "is_public", server_default=None)

    # --- pokeset: add author_id + FK to user.id ---
    # Step 1: add column
    op.add_column("pokeset", sa.Column("author_id", sa.Integer(), nullable=True))

    # Step 2: add FK + index
    with op.batch_alter_table("pokeset") as batch_op:
        batch_op.create_foreign_key(
            "fk_pokeset_author",
            "user",
            ["author_id"],
            ["id"],
            ondelete="RESTRICT",
        )

    op.create_index("ix_pokeset_author_id", "pokeset", ["author_id"])


def downgrade() -> None:
    op.drop_index("ix_pokeset_author_id", table_name="pokeset")

    with op.batch_alter_table("pokeset") as batch_op:
        batch_op.drop_constraint("fk_pokeset_author", type_="foreignkey")

    op.drop_column("pokeset", "author_id")
    op.drop_column("user", "is_public")