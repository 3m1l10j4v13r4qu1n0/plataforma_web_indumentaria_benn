from typing import Protocol

from app.domain.models.categoria import Categoria


class ICategoriaRepository(Protocol):
    """Puerto que define las operaciones de persistencia para Categoria."""

    async def obtener_por_id(self, categoria_id: int) -> Categoria:
        """Obtiene una categoría por su identificador.

        Args:
            categoria_id: Identificador autoincremental de la categoría.

        Returns:
            La entidad Categoria correspondiente.

        Raises:
            CategoriaNoEncontradaError: Si no existe una categoría con
                ese id.
        """
        ...

    async def listar_todas(self) -> list[Categoria]:
        """Lista todas las categorías del catálogo.

        Returns:
            Lista de entidades Categoria.
        """
        ...