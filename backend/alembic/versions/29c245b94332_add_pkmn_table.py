"""add pkmn table

Revision ID: 29c245b94332
Revises: 7e052996dd76
Create Date: 2026-02-03 17:39:45.402623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29c245b94332'
down_revision: Union[str, None] = '7e052996dd76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
