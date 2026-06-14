from typing import Any, Dict, List

from app.application.dtos.cambio_dto import SolicitarCambioCommand
from app.domain.exceptions import (
    ProductoNoEncontradoError,
    ProductoNoPerteneceAVentaError,
    VentaNoEncontradaError,
)
from app.domain.models.condicion_producto import CondicionProducto
from app.domain.ports.i_producto_repository import IProductoRepository
from app.domain.ports.i_venta_repository import IVentaRepository


class SolicitarCambioUseCase:
    """
    Caso de Uso para validar la elegibilidad de una venta y sus productos para un cambio.
    Orquesta las reglas de HU-02 (plazo), HU-03 (condición) y HU-04 (pertenencia al ticket).
    """

    def __init__(
        self,
        venta_repository: IVentaRepository,
        producto_repository: IProductoRepository,
    ):
        # DIP: Solo dependemos de abstracciones (Protocol)
        self._venta_repository = venta_repository
        self._producto_repository = producto_repository

    async def execute(self, command: SolicitarCambioCommand) -> Dict[str, Any]:
        # 1. Recuperar la venta por su comprobante
        venta = await self._venta_repository.obtener_por_numero_ticket(
            command.numero_ticket
        )
        if not venta:
            raise VentaNoEncontradaError(command.numero_ticket)

        # 2. Validar elegibilidad temporal y de estado de la venta (HU-02)
        # Lanza PlazoDeCambioVencidoError o ValueError si no es CONFIRMADA
        venta.validar_elegibilidad_para_cambio(command.fecha_solicitud)

        # 3. Validar cada producto solicitado para cambio (HU-03 y HU-04)
        items_validados = []
        for item_solicitado in command.items_a_cambiar:
            # 3.1 Verificar que el producto existe en el sistema
            producto = await self._producto_repository.obtener_por_id(
                item_solicitado.producto_id
            )
            if not producto:
                # Nota: ProductoNoEncontradoError espera un código, pero podemos adaptar el mensaje
                # o usar el ID si el repositorio lo permite. Usaremos el ID como fallback.
                raise ProductoNoEncontradoError(item_solicitado.producto_id)

            # 3.2 Verificar que el producto pertenece a esta venta específica (HU-04)
            producto_en_venta = next(
                (
                    item
                    for item in venta.items
                    if item.producto_id == item_solicitado.producto_id
                ),
                None,
            )
            if not producto_en_venta:
                raise ProductoNoPerteneceAVentaError(
                    producto_id=item_solicitado.producto_id,
                    numero_ticket=command.numero_ticket,
                )

            # 3.3 Validar la condición del producto (HU-03)
            # La instanciación del Value Object lanzará ProductoNoAptoParaCambioError
            # automáticamente si condicion_declarada != "NUEVO_CON_ETIQUETA"
            condicion = CondicionProducto(
                estado_declarado=item_solicitado.condicion_declarada
            )

            items_validados.append(
                {
                    "producto_id": item_solicitado.producto_id,
                    "nombre": producto.nombre,
                    "cantidad_original": producto_en_venta.cantidad,
                    "condicion_validada": condicion.estado_declarado,
                }
            )

        # 4. Retornar resultado de la validación para que la UI o el siguiente paso del flujo continúe
        return {
            "venta_id": venta.id,
            "numero_ticket": venta.numero_ticket,
            "fecha_compra": venta.fecha_hora,
            "estado": venta.estado,
            "items_validados": items_validados,
            "mensaje": "Venta y productos elegibles para cambio. Proceda con la selección del nuevo producto.",
        }
