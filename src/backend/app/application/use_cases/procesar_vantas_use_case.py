# Caso de uso simplificado HU-05

import uuid
from datetime import datetime
from typing import List

from app.application.dtos.venta_dto import CrearVentaCommand, ItemVentaDTO
from app.domain.exceptions import (
    EstadoProductoInvalidoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
    UsuarioNoAutorizadoError,
)
from app.domain.models.descuento import Descuento
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.venta import Venta
from app.domain.ports.i_producto_repository import IProductoRepository
from app.domain.ports.i_usuario_repository import IUsuarioRepository
from app.domain.ports.i_venta_repository import IVentaRepository


class ProcesarVentaUseCase:
    """
    Caso de Uso para procesar una venta completa.
    Orquesta la validación de stock (HU-01) y la autorización de descuentos (HU-05).
    """

    def __init__(
        self,
        producto_repository: IProductoRepository,
        venta_repository: IVentaRepository,
        usuario_repository: IUsuarioRepository,
    ):
        self._producto_repository = producto_repository
        self._venta_repository = venta_repository
        self._usuario_repository = usuario_repository

    async def execute(self, command: CrearVentaCommand) -> Venta:
        if not command.items:
            raise ValueError("La venta debe contener al menos un item.")

        # FASE 1: Validación de Autorización de Descuento (HU-05)
        # Si el descuento supera el 20%, verificamos que el ID proporcionado corresponda a un Gerente.
        if command.porcentaje_descuento > 20.0:
            if not command.gerente_autorizacion_id:
                # Si no hay ID, el Value Object Descuento lanzará DescuentoExcedeLimiteError más adelante.
                # Pero podemos validar el rol proactivamente si se proporciona un ID.
                pass
            else:
                es_gerente = await self._usuario_repository.es_gerente(
                    command.gerente_autorizacion_id
                )
                if not es_gerente:
                    raise UsuarioNoAutorizadoError(
                        usuario_id=command.gerente_autorizacion_id,
                        rol_requerido="GERENTE",
                    )

        # FASE 2: Validación de Stock y Estado (HU-01)
        detalles: List[DetalleVenta] = []
        for item in command.items:
            producto = await self._producto_repository.obtener_por_id(item.producto_id)

            if not producto:
                raise ProductoNoEncontradoError(item.producto_id)

            if producto.estado != "ACTIVO":
                raise EstadoProductoInvalidoError(item.producto_id, producto.estado)

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

        # FASE 3: Creación de la Entidad de Dominio
        # El Value Object Descuento validará sus propias invariantes (rango 0-100%, y requerimiento de gerente si > 20%)
        descuento = Descuento(
            porcentaje=command.porcentaje_descuento,
            gerente_autorizacion_id=command.gerente_autorizacion_id,
        )

        nueva_venta = Venta(
            id=str(uuid.uuid4()),
            fecha_hora=datetime.utcnow(),
            vendedor_id=command.vendedor_id,
            estado="CONFIRMADA",
            items=detalles,
            descuento=descuento,
        )

        # FASE 4: Ejecución Atómica (Descuento de stock y Persistencia)
        # Nota: En un patrón Unit of Work estricto, esto se haría en una sola transacción.
        # Aquí confiamos en que los repositorios comparten la misma AsyncSession.
        for item in command.items:
            producto = await self._producto_repository.obtener_por_id(item.producto_id)
            nuevo_stock = producto.stock_actual - item.cantidad
            await self._producto_repository.actualizar_stock(
                item.producto_id, nuevo_stock
            )

        venta_guardada = await self._venta_repository.crear_venta(nueva_venta)

        return venta_guardada
