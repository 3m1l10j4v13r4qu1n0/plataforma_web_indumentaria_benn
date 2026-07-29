from app.domain.exceptions import ProductoNoEncontradoError
from app.domain.models.producto import Producto
from app.domain.ports.i_producto_repository import IProductoRepository


class ConsultarStockProductoUseCase:
    """Caso de uso para consultar stock disponible por nombre o código."""

    def __init__(self, producto_repository: IProductoRepository):
        self._producto_repository = producto_repository

    async def execute(self, query: str) -> list[Producto]:
        if not query or not query.strip():
            raise ValueError("La búsqueda no puede estar vacía.")

        productos = await self._producto_repository.buscar_por_nombre_o_codigo(query)

        if not productos:
            raise ProductoNoEncontradoError(query)

        return productos
