from dataclasses import dataclass


@dataclass
class DetalleVenta:
    producto_id: str
    cantidad: int

    def __post_init__(self):
        if self.cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor a cero.")
