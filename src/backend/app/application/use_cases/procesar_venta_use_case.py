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
from app.domain.models.movimiento_stock import MovimientoStock
from app.domain.models.venta import Venta
from app.domain.ports.i_movimiento_stock_repository import IMovimientoStockRepository
from app.domain.ports.i_producto_repository import IProductoRepository
from app.domain.ports.i_unit_of_work import IUnitOfWork
from app.domain.ports.i_usuario_repository import IUsuarioRepository
from app.domain.ports.i_venta_repository import IVentaRepository
from app.domain.services.generador_ticket import (
    generar_numero_ticket,
)  # <-- NUEVO: Importación del servicio puro


class ProcesarVentaUseCase:
    def __init__(
        self,
        producto_repository: IProductoRepository,
        venta_repository: IVentaRepository,
        usuario_repository: IUsuarioRepository,
        movimiento_stock_repository: IMovimientoStockRepository,
        unit_of_work: IUnitOfWork,
    ):
        self._producto_repository = producto_repository
        self._venta_repository = venta_repository
        self._usuario_repository = usuario_repository
        self._movimiento_stock_repository = movimiento_stock_repository
        self._unit_of_work = unit_of_work

    async def execute(self, command: CrearVentaCommand) -> Venta:
        if not command.items:
            raise ValueError("La venta debe contener al menos un item.")

        # FASE 1: Validación de Autorización de Descuento (HU-05)
        if command.porcentaje_descuento > 20.0:
            if command.gerente_autorizacion_id:
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

        # FASE 3: Preparación de Entidades de Dominio
        venta_id = str(uuid.uuid4())

        # --- HU-07: Generación automática del número de ticket ---
        numero_ticket = generar_numero_ticket()

        descuento = Descuento(
            porcentaje=command.porcentaje_descuento,
            gerente_autorizacion_id=command.gerente_autorizacion_id,
        )
        nueva_venta = Venta(
            id=venta_id,
            fecha_hora=datetime.utcnow(),
            vendedor_id=command.vendedor_id,
            numero_ticket=numero_ticket,  # <-- Asignación del ticket generado
            estado="CONFIRMADA",
            items=detalles,
            descuento=descuento,
        )

        # FASE 4: Ejecución Atómica (ACID)
        try:
            for item in command.items:
                # 4.1 Descontar stock (sin commit interno en el repositorio)
                producto = await self._producto_repository.obtener_por_id(
                    item.producto_id
                )
                nuevo_stock = producto.stock_actual - item.cantidad
                await self._producto_repository.actualizar_stock(
                    item.producto_id, nuevo_stock
                )

                # 4.2 Registrar movimiento de stock (HU-08)
                movimiento = MovimientoStock(
                    id=str(uuid.uuid4()),
                    producto_id=item.producto_id,
                    cantidad=-item.cantidad,  # Negativo: egreso por venta
                    tipo_movimiento="VENTA",
                    referencia_id=venta_id,
                    usuario_id=command.vendedor_id,
                    fecha_hora=datetime.utcnow(),
                )
                await self._movimiento_stock_repository.registrar_movimiento(movimiento)

            # 4.3 Persistir la venta
            await self._venta_repository.crear_venta(nueva_venta)

            # 4.4 Confirmar transacción (todas las operaciones se guardan juntas o se revierten)
            await self._unit_of_work.commit()

        except Exception:
            # Rollback de infraestructura ante cualquier fallo (incluyendo excepciones de dominio)
            await self._unit_of_work.rollback()
            raise  # Deja que la excepción de dominio burbujee a handlers.py

        return nueva_venta
