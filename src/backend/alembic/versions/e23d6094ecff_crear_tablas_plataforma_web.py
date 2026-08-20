"""crear tablas plataforma web

Revision ID: e23d6094ecff
Revises:
Create Date: 2026-07-15 15:54:49.789704

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e23d6094ecff"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "productos",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("codigo", sa.String(length=50), nullable=False, unique=True),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("precio", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("stock_actual", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("categoria", sa.String(length=100), nullable=False),
        sa.Column(
            "estado", sa.String(length=20), nullable=False, server_default="ACTIVO"
        ),
        sa.CheckConstraint("stock_actual >= 0", name="check_stock_no_negativo"),
    )
    op.create_index("ix_producto_codigo", "productos", ["codigo"])

    op.create_table(
        "ventas",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("fecha_hora", sa.DateTime(), nullable=False),
        sa.Column("vendedor_id", sa.String(length=36), nullable=False),
        sa.Column(
            "estado", sa.String(length=20), nullable=False, server_default="PENDIENTE"
        ),
    )

    op.create_table(
        "detalles_venta",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column(
            "venta_id", sa.String(length=36), sa.ForeignKey("ventas.id"), nullable=False
        ),
        sa.Column(
            "producto_id",
            sa.String(length=36),
            sa.ForeignKey("productos.id"),
            nullable=False,
        ),
        sa.Column("cantidad", sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("detalles_venta")
    op.drop_table("ventas")
    op.drop_index("ix_producto_codigo", table_name="productos")
    op.drop_table("productos")
