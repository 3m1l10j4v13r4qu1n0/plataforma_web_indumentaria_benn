from dataclasses import dataclass
from app.domain.exceptions import DomainException

@dataclass
class DetalleVenta:
    producto_id: str
    cantidad: int

    def __post_init__(self):
        if self.cantidad <= 0:
            raise DomainException(
                "La cantidad a vender debe ser mayor a cero."
                )
