from dataclasses import dataclass
from enum import Enum

from app.domain.exceptions import DomainException, StockInsuficienteError
           

class EstadoProducto(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"


@dataclass
class Producto:
    id: int
    codigo: str
    nombre: str
    categoria_id: int
    precio: int
    stock_actual: int
    estado: EstadoProducto

    def __post_init__(self):

        if self.stock_actual < 0:
            raise DomainException(
                "El stock actual no puede ser negativo."
            )
                
        
        if self.precio <= 0:
            raise DomainException("El precio debe ser mayor a cero.")

    def esta_activo(self) -> bool:
        return self.estado == EstadoProducto.ACTIVO

    
    def hay_stock_suficiente(self, cantidad: int) -> bool:
        return self.esta_activo() and self.stock_actual >= cantidad

    def descontar_stock(self, cantidad: int):
        if not self.hay_stock_suficiente(cantidad):

            raise StockInsuficienteError(
                self.id, self.nombre, self.stock_actual, cantidad
            )
        self.stock_actual -= cantidad
