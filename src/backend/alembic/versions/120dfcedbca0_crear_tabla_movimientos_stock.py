"""crear tabla movimientos_stock

Revision ID: 120dfcedbca0
Revises: f7a2c9d41e08
Create Date: 2026-08-24 13:03:24.965865

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "120dfcedbca0"
down_revision: Union[str, Sequence[str], None] = "f7a2c9d41e08"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "movimientos_stock",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("producto_id", sa.String(length=36), nullable=False),
        sa.Column("tipo_movimiento", sa.String(length=20), nullable=False),
        sa.Column("cantidad", sa.Integer(), nullable=False),
        sa.Column("fecha_hora", sa.DateTime(), nullable=False),
        sa.Column("documento_referencia_id", sa.String(length=36), nullable=True),
        sa.CheckConstraint(
            "(tipo_movimiento = 'VENTA' AND cantidad < 0) "
            "OR (tipo_movimiento <> 'VENTA' AND cantidad > 0)",
            name="check_signo_cantidad_consistente",
        ),
        sa.CheckConstraint(
            "tipo_movimiento IN ('VENTA', 'DEVOLUCION', 'AJUSTE')",
            name="check_tipo_movimiento_valido",
        ),
        sa.ForeignKeyConstraint(["producto_id"], ["productos.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_movimiento_stock_documento_ref",
        "movimientos_stock",
        ["documento_referencia_id"],
        unique=False,
    )
    op.create_index(
        "ix_movimiento_stock_producto",
        "movimientos_stock",
        ["producto_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_movimiento_stock_producto", table_name="movimientos_stock")
    op.drop_index("ix_movimiento_stock_documento_ref", table_name="movimientos_stock")
    op.drop_table("movimientos_stock")
