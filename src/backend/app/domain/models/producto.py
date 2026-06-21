from dataclasses import dataclass
from typing import Literal

from app.domain.exceptions import DomainException


@dataclass
class Producto:
    id: str
    codigo: str
    nombre: str
    precio: float
    categoria: str
    stock_actual: int
    estado: Literal["ACTIVO", "INACTIVO"]

    def __post_init__(self):
        if self.stock_actual < 0:
            raise DomainException("El stock actual no puede ser negativo.")
        if self.estado not in ("ACTIVO", "INACTIVO"):
            raise DomainException(
                "El estado del producto debe ser 'ACTIVO' o 'INACTIVO'."
            )
        if not self.categoria.strip():
            raise DomainException("La categoría no puede estar vacía.")

    def hay_stock_suficiente(self, cantidad: int) -> bool:
        return self.estado == "ACTIVO" and self.stock_actual >= cantidad

    def descontar_stock(self, cantidad: int):
        if not self.hay_stock_suficiente(cantidad):
            from app.domain.exceptions import StockInsuficienteError

            raise StockInsuficienteError(
                self.id, self.nombre, self.stock_actual, cantidad
            )
        self.stock_actual -= cantidad
