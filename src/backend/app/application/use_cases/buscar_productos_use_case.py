from typing import List

from app.application.dtos.producto_dto import (
    BuscarProductosCommand,
    BuscarProductosResponseDTO,
    ProductoStockResumenDTO,
)
from app.domain.ports.i_producto_repository import IProductoRepository


class BuscarProductosUseCase:
    """
    Caso de Uso para consultar productos disponibles por nombre o código (HU-06).
    Orquesta la búsqueda y mapea las entidades de dominio a DTOs de aplicación.
    """

    def __init__(self, producto_repository: IProductoRepository):
        # DIP: Solo dependemos de la abstracción (Protocol)
        self._producto_repository = producto_repository

    async def execute(
        self, command: BuscarProductosCommand
    ) -> BuscarProductosResponseDTO:
        # 1. Delegar la búsqueda al repositorio (la infraestructura maneja ilike/exact match)
        productos_dominio = await self._producto_repository.buscar_por_nombre_o_codigo(
            command.query
        )

        # 2. Mapear Entidades de Dominio a DTOs de Aplicación
        productos_dto = [
            ProductoStockResumenDTO(
                producto_id=prod.id,
                codigo=prod.codigo,
                nombre=prod.nombre,
                stock_actual=prod.stock_actual,
                estado=prod.estado,
            )
            for prod in productos_dominio
        ]

        # 3. Generar mensaje contextual según el resultado
        if not productos_dto:
            mensaje = (
                f"No se encontraron productos que coincidan con '{command.query}'."
            )
        else:
            mensaje = f"Se encontraron {len(productos_dto)} producto(s)."

        return BuscarProductosResponseDTO(productos=productos_dto, mensaje=mensaje)
