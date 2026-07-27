from dataclasses import dataclass

from app.domain.exceptions import CategoriaInvalidaError


@dataclass
class Categoria:
    """Entidad de dominio que representa una categoría de producto.

    A diferencia de Producto, usa id autoincremental (int) en lugar de
    UUID por ser un catálogo interno de bajo volumen, sin necesidad de
    identificadores distribuidos.

    Attributes:
        id: Identificador autoincremental de la categoría.
        nombre: Nombre descriptivo y único de la categoría.
    """

    id: int
    nombre: str

    def __post_init__(self):
        """Valida los invariantes de la entidad al construirla.

        Raises:
            CategoriaInvalidaError: Si el nombre está vacío o solo
                contiene espacios en blanco.
        """
        if not self.nombre or not self.nombre.strip():
            raise CategoriaInvalidaError(
                "El nombre de la categoría no puede estar vacío."
            )