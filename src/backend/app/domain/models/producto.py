from dataclasses import dataclass
from enum import Enum

from app.domain.exceptions import DomainException, StockInsuficienteError


class EstadoProducto(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"


@dataclass
class Producto:
    id: str
    codigo: str
    nombre: str
    categoria: str
    precio: int
    stock_actual: int
    estado: EstadoProducto

    def __post_init__(self):

        if self.stock_actual < 0:
            raise DomainException("El stock actual no puede ser negativo.")

        if self.precio <= 0:
            raise DomainException("El precio debe ser mayor a cero.")

    def esta_activo(self) -> bool:
        return self.estado == EstadoProducto.ACTIVO

    def hay_stock_suficiente(self, cantidad: int) -> bool:
        return self.esta_activo() and self.stock_actual >= cantidad

    def descontar_stock(self, cantidad: int) -> None:
        """Descuenta unidades del stock actual validando que alcance.

        Args:
            cantidad: Unidades a descontar; debe ser mayor a cero.

        Raises:
            DomainException: Si la cantidad no es mayor a cero.
            StockInsuficienteError: Si el stock no alcanza para la venta.
        """
        if cantidad <= 0:
            raise DomainException("La cantidad a descontar debe ser mayor a cero.")

        if not self.hay_stock_suficiente(cantidad):

            raise StockInsuficienteError(
                self.id, self.nombre, self.stock_actual, cantidad
            )
        self.stock_actual -= cantidad

    def incrementar_stock(self, cantidad: int) -> None:
        """Incrementa el stock actual del producto (devoluciones y ajustes).

        Args:
            cantidad: Unidades a sumar; debe ser mayor a cero.

        Raises:
            DomainException: Si la cantidad no es mayor a cero.
        """
        if cantidad <= 0:
            raise DomainException("La cantidad a incrementar debe ser mayor a cero.")

        self.stock_actual += cantidad
