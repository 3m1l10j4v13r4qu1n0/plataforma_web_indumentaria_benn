from typing import Protocol

from app.domain.models.categoria import Categoria


class ICategoriaRepository(Protocol):
    async def obtener_por_id(self, categoria_id: int) -> Categoria:
        """Debe lanzar CategoriaNoEncontradaError si no existe."""
        ...

    async def listar_todas(self) -> list[Categoria]:
        ...