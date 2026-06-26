import uuid
from datetime import datetime
from typing import List

from app.application.dtos.venta_dto import CrearVentaCommand, ItemVentaDTO
from app.domain.exceptions import (
    ProductoInvalidoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
)
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.venta import Venta
from app.domain.ports.i_producto_repository import IProductoRepository
from app.domain.ports.i_venta_repository import IVentaRepository


class ValidarStockVentaUseCase:
    """
    Caso de Uso para validar stock y procesar una venta.
    Orquesta la lógica de negocio y deja que las excepciones de dominio burbujeen
    hacia el manejador global de errores (Paso 5).
    """

    def __init__(
        self,
        producto_repository: IProductoRepository,
        venta_repository: IVentaRepository,
    ):
        self._producto_repository = producto_repository
        self._venta_repository = venta_repository

    async def execute(self, command: CrearVentaCommand) -> Venta:
        if not command.items:
            raise ValueError("La venta debe contener al menos un item.")

        venta_id = str(uuid.uuid4())
        detalles: List[DetalleVenta] = []

        # FASE 1: Validación y Bloqueo de Filas (Fetch con for_update)
        # Se valida cada item antes de realizar cualquier modificación.
        for item in command.items:
            producto = await self._producto_repository.obtener_por_id(item.producto_id)

            if not producto:
                raise ProductoNoEncontradoError(item.producto_id)

            if producto.estado != "ACTIVO":
                raise ProductoInvalidoError(item.producto_id, producto.estado)

            if producto.stock_actual < item.cantidad:
                raise StockInsuficienteError(
                    producto_id=item.producto_id,
                    nombre_producto=producto.nombre,
                    stock_actual=producto.stock_actual,
                    cantidad_solicitada=item.cantidad,
                )

            detalles.append(
                DetalleVenta(producto_id=item.producto_id, cantidad=item.cantidad)
            )

        # FASE 2: Ejecución Atómica (Descuento y Registro)
        # Nota de Arquitectura: Para garantizar una transacción ACID estricta
        # a través de múltiples agregados (Producto y Venta), lo ideal es usar
        # un patrón Unit of Work que haga un único commit al final.
        # En este scaffold, confiamos en que el repositorio comparte la misma
        # sesión de SQLAlchemy y maneja la atomicidad.

        for item in command.items:
            # Volvemos a obtener el producto (ya bloqueado por for_update en la sesión actual)
            # para asegurar el estado más reciente antes de descontar.
            producto = await self._producto_repository.obtener_por_id(item.producto_id)
            nuevo_stock = producto.stock_actual - item.cantidad

            await self._producto_repository.actualizar_stock(
                item.producto_id, nuevo_stock
            )

        # FASE 3: Creación de la Entidad de Dominio y Persistencia
        nueva_venta = Venta(
            id=venta_id,
            fecha_hora=datetime.utcnow(),
            vendedor_id=command.vendedor_id,
            estado="CONFIRMADA",  # Se confirma directamente si pasa todas las validaciones
            items=detalles,
        )

        venta_guardada = await self._venta_repository.crear_venta(nueva_venta)

        return venta_guardada
