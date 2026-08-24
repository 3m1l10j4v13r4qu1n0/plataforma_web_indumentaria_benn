"""crear tabla descuentos

Revision ID: f7a2c9d41e08
Revises: 7645ca7d4256
Create Date: 2026-08-24 13:03:24.965865

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f7a2c9d41e08"
down_revision: Union[str, Sequence[str], None] = "7645ca7d4256"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "descuentos",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("venta_id", sa.String(length=36), nullable=False),
        sa.Column("porcentaje", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("monto_descuento", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("motivo", sa.String(length=255), nullable=False),
        sa.Column("autorizado_por", sa.String(length=36), nullable=True),
        sa.Column("fecha_aplicacion", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["venta_id"], ["ventas.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("venta_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("descuentos")
