from app.domain.models.movimiento_stock import MovimientoStock
from app.domain.ports.i_movimiento_stock_repository import IMovimientoStockRepository
from app.infrastructure.database.orm_models.movimiento_stock_orm import (
    MovimientoStockORM,
)
from sqlalchemy.ext.asyncio import AsyncSession


class MovimientoStockRepository(IMovimientoStockRepository):
    def __init__(self, session: AsyncSession):
        # Inyectamos la sesión para compartir la misma transacción que otros repositorios
        self.session = session

    async def registrar_movimiento(self, movimiento: MovimientoStock) -> None:
        """
        Registra un movimiento de stock en la base de datos.

        NOTA DE ATOMICIDAD: Este método NO ejecuta `commit`.
        Se añade a la sesión actual, y el commit se realizará a nivel del Caso de Uso
        para garantizar que la actualización del stock del producto y el registro
        de este movimiento sean atómicos (ACID).
        """
        orm_movimiento = MovimientoStockORM(
            id=movimiento.id,
            producto_id=movimiento.producto_id,
            cantidad=movimiento.cantidad,
            tipo_movimiento=movimiento.tipo_movimiento,
            referencia_id=movimiento.referencia_id,
            fecha_hora=movimiento.fecha_hora,
            usuario_id=movimiento.usuario_id,
        )

        self.session.add(orm_movimiento)
        # No hay commit aquí. El Caso de Uso orquestará el commit final.
