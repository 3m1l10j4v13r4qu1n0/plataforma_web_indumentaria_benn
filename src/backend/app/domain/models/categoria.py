from dataclasses import dataclass

from app.domain.exceptions import CategoriaInvalidaError


@dataclass
class Categoria:
    """
    Entidad de catálogo interno. A diferencia de Producto, usa id
    autoincremental (int) en lugar de UUID por ser un catálogo de
    bajo volumen gestionado internamente, sin necesidad de
    identificadores distribuidos.
    """
    id: int
    nombre: str

    def __post_init__(self):
        if not self.nombre or not self.nombre.strip():
            raise CategoriaInvalidaError(
                "El nombre de la categoría no puede estar vacío."
            )