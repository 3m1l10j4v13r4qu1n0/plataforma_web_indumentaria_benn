import uuid
from datetime import datetime, UTC
from decimal import Decimal


from app.application.dtos.venta_dto import (
    CrearVentaCommand,
    ItemVentaResultado,
    ResultadoVenta,
)
from app.domain.exceptions import (
    ProductoInvalidoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
)
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.movimiento_stock import MovimientoStock, TipoMovimiento
from app.domain.models.producto import EstadoProducto
from app.domain.models.venta import EstadoVenta, Venta
from app.domain.ports.i_generador_numero_ticket import IGeneradorNumeroTicket
from app.domain.ports.i_movimiento_stock_repository import IMovimientoStockRepository
from app.domain.ports.i_producto_repository import IProductoRepository
from app.domain.ports.i_venta_repository import IVentaRepository


class ValidarStockVentaUseCase:
    """
    Caso de Uso para validar stock, generar el ticket y procesar una venta.
    Orquesta la lógica de negocio y deja que las excepciones de dominio burbujeen
    hacia el manejador global de errores (Paso 5).
    """

    def __init__(
        self,
        producto_repository: IProductoRepository,
        venta_repository: IVentaRepository,
        generador_numero_ticket: IGeneradorNumeroTicket,
        movimiento_stock_repository: IMovimientoStockRepository,
    ):
        self._producto_repository = producto_repository
        self._venta_repository = venta_repository
        self._generador_numero_ticket = generador_numero_ticket
        self._movimiento_stock_repository = movimiento_stock_repository

    async def execute(self, command: CrearVentaCommand) -> ResultadoVenta:
        """Valida el stock, confirma la venta y devuelve el resultado listo para presentar.

        Args:
            command: Datos de la venta a procesar (vendedor e ítems).

        Returns:
            Un `ResultadoVenta` con los datos del comprobante y los nombres
            de los productos resueltos, sin exponer entidades de dominio.

        Raises:
            ProductoNoEncontradoError: Si algún ítem referencia un producto inexistente.
            ProductoInvalidoError: Si algún producto no está activo.
            StockInsuficienteError: Si algún producto no tiene stock suficiente.
        """
        if not command.items:
            raise ValueError("La venta debe contener al menos un item.")

        venta_id = str(uuid.uuid4())
        detalles: list[DetalleVenta] = []
        nombres: dict[str, str] = {}

        # FASE 1: Validación y Bloqueo de Filas (Fetch con for_update)
        # Se valida cada item antes de realizar cualquier modificación.
        # Se congela el precio unitario como snapshot histórico (HU-07)
        # y se captura el nombre para el resultado de presentación.
        for item in command.items:
            producto = await self._producto_repository.obtener_por_id(item.producto_id)

            if not producto:
                raise ProductoNoEncontradoError(item.producto_id)

            if producto.estado != EstadoProducto.ACTIVO:
                raise ProductoInvalidoError(item.producto_id, producto.estado)

            if producto.stock_actual < item.cantidad:
                raise StockInsuficienteError(
                    producto_id=item.producto_id,
                    nombre_producto=producto.nombre,
                    stock_actual=producto.stock_actual,
                    cantidad_solicitada=item.cantidad,
                )

            nombres[item.producto_id] = producto.nombre
            detalles.append(
                DetalleVenta(
                    producto_id=item.producto_id,
                    cantidad=item.cantidad,
                    precio_unitario=Decimal(producto.precio),
                )
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
            if not producto:
                raise ProductoNoEncontradoError(item.producto_id)

            nuevo_stock = producto.stock_actual - item.cantidad

            await self._producto_repository.actualizar_stock(
                item.producto_id, nuevo_stock
            )

            # HU-08: cada descuento queda auditado en movimientos_stock,
            # referenciando la venta que lo originó.
            movimiento = MovimientoStock.registrar(
                id=str(uuid.uuid4()),
                producto_id=item.producto_id,
                tipo_movimiento=TipoMovimiento.VENTA,
                cantidad=item.cantidad,
                fecha_hora=datetime.now(UTC).replace(tzinfo=None),
                documento_referencia_id=venta_id,
            )
            await self._movimiento_stock_repository.registrar(movimiento)

        # FASE 3: Creación de la Entidad de Dominio y Persistencia
        # El número de ticket se genera automáticamente al confirmar la
        # venta (nunca lo ingresa el usuario) y el total se calcula con los
        # precios congelados.
        numero_ticket = await self._generador_numero_ticket.generar()

        nueva_venta = Venta(
            id=venta_id,
            # Se persiste en UTC naive para coincidir con la columna
            # TIMESTAMP WITHOUT TIME ZONE de la base de datos.
            fecha_hora=datetime.now(UTC).replace(tzinfo=None),
            vendedor_id=command.vendedor_id,
            estado=EstadoVenta.CONFIRMADA,
            numero_ticket=numero_ticket,
            items=detalles,
        )
        nueva_venta.total = nueva_venta.calcular_total()

        venta_guardada = await self._venta_repository.crear_venta(nueva_venta)

        return ResultadoVenta(
            id=venta_guardada.id,
            fecha_hora=venta_guardada.fecha_hora,
            vendedor_id=venta_guardada.vendedor_id,
            estado=venta_guardada.estado,
            numero_ticket=venta_guardada.numero_ticket,
            total=venta_guardada.total,
            items=[
                ItemVentaResultado(
                    producto_id=detalle.producto_id,
                    nombre=nombres[detalle.producto_id],
                    cantidad=detalle.cantidad,
                    precio_unitario=detalle.precio_unitario,
                )
                for detalle in venta_guardada.items
            ],
        )
