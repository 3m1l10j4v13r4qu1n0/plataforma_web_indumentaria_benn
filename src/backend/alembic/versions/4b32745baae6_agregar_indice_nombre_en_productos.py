"""agregar indice nombre en productos

Revision ID: 4b32745baae6
Revises: e23d6094ecff
Create Date: 2026-08-21 18:40:29.341705

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "4b32745baae6"
down_revision: Union[str, Sequence[str], None] = "e23d6094ecff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index("ix_producto_nombre", "productos", ["nombre"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_producto_nombre", table_name="productos")
