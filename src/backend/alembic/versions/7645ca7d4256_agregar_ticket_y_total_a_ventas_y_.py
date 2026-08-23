"""agregar ticket y total a ventas y precio unitario a detalles

Revision ID: 7645ca7d4256
Revises: 4b32745baae6
Create Date: 2026-08-21 21:52:33.133690

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7645ca7d4256"
down_revision: Union[str, Sequence[str], None] = "4b32745baae6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "detalles_venta",
        sa.Column(
            "precio_unitario",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "ventas", sa.Column("numero_ticket", sa.String(length=30), nullable=True)
    )
    op.add_column(
        "ventas", sa.Column("total", sa.Numeric(precision=12, scale=2), nullable=True)
    )
    op.create_unique_constraint("uq_ventas_numero_ticket", "ventas", ["numero_ticket"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_ventas_numero_ticket", "ventas", type_="unique")
    op.drop_column("ventas", "total")
    op.drop_column("ventas", "numero_ticket")
    op.drop_column("detalles_venta", "precio_unitario")
