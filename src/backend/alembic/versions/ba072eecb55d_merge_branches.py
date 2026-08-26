"""merge branches

Revision ID: ba072eecb55d
Revises: 120dfcedbca0, 3e1674bc0a91
Create Date: 2026-08-26 07:21:25.022641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba072eecb55d'
down_revision: Union[str, Sequence[str], None] = ('120dfcedbca0', '3e1674bc0a91')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
