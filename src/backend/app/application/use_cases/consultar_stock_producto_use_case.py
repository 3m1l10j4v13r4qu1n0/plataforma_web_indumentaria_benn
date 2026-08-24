"""Caso de Uso: consultar el stock actual de un producto por su código (HU-01/HU-06)."""

from app.domain.exceptions import ProductoNoEncontradoError
from app.domain.models.producto import Producto
from app.domain.ports.i_producto_repository import IProductoRepository


class ConsultarStockProductoUseCase:
    """
    Caso de Uso para obtener el stock en tiempo real de un producto.

    Encapsula la búsqueda por código y la validación de existencia, dejando
    que las excepciones de dominio burbujeen hacia el manejador global de
    errores. El router solo delega y mapea a su esquema de respuesta.
    """

    def __init__(self, producto_repository: IProductoRepository):
        self._producto_repository = producto_repository

    async def execute(self, codigo: str) -> Producto:
        """Obtiene el producto correspondiente al código indicado.

        Args:
            codigo: Código único del producto a consultar.

        Returns:
            La entidad de dominio del producto con su stock actual.

        Raises:
            ProductoNoEncontradoError: Si no existe un producto con ese código.
        """
        producto = await self._producto_repository.obtener_por_codigo(codigo)

        if not producto:
            raise ProductoNoEncontradoError(codigo)

        return producto
