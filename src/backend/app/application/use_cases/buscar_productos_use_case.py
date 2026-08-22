from app.domain.exceptions import BusquedaInvalidaError
from app.domain.models.producto import Producto
from app.domain.ports.i_producto_repository import IProductoRepository

MINIMO_CARACTERES_BUSQUEDA = 3


class BuscarProductosUseCase:
    """Caso de uso para buscar productos activos por nombre o código.

    Permite al vendedor consultar el stock disponible informando un término
    de búsqueda que se contrasta contra el nombre y el código de los productos.
    """

    def __init__(self, producto_repository: IProductoRepository):
        self._producto_repository = producto_repository

    async def execute(self, query: str) -> list[Producto]:
        """Busca productos activos cuyo nombre o código coincida con el término.

        Args:
            query: Término de búsqueda ingresado por el vendedor.

        Returns:
            Lista de productos activos que coinciden. Vacía si no hay
            coincidencias (no se considera un error).

        Raises:
            BusquedaInvalidaError: Si el término tiene menos de 3 caracteres.
        """
        termino = query.strip()

        if len(termino) < MINIMO_CARACTERES_BUSQUEDA:
            raise BusquedaInvalidaError(query)

        return await self._producto_repository.buscar_por_nombre_o_codigo(termino)
