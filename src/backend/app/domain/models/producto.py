from dataclasses import dataclass
from enum import Enum

from app.domain.exceptions import DomainException, StockInsuficienteError


class EstadoProducto(str, Enum):
    """Estados posibles de un producto en el catálogo."""

    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"


@dataclass
class Producto:
    """Entidad de dominio que representa un producto del catálogo.

    Attributes:
        id: Identificador único del producto (UUID en formato string).
        codigo: Código de barras o SKU del producto.
        nombre: Nombre descriptivo del producto.
        categoria_id: Identificador de la categoría a la que pertenece.
        precio: Precio unitario del producto, debe ser mayor a cero.
        stock_actual: Cantidad disponible en inventario.
        estado: Estado actual del producto (ACTIVO/INACTIVO).
    """

    id: str
    codigo: str
    nombre: str
    categoria_id: int
    precio: int
    stock_actual: int
    estado: EstadoProducto

    def __post_init__(self):
        """Valida los invariantes de la entidad al construirla.

        Raises:
            DomainException: Si el stock es negativo o el precio no es
                mayor a cero.
        """
        if self.stock_actual < 0:
            raise DomainException(
                "El stock actual no puede ser negativo."
            )

        if self.precio <= 0:
            raise DomainException("El precio debe ser mayor a cero.")

    def esta_activo(self) -> bool:
        """Indica si el producto se encuentra activo.

        Returns:
            True si el estado del producto es ACTIVO, False en caso
            contrario.
        """
        return self.estado == EstadoProducto.ACTIVO

    def hay_stock_suficiente(self, cantidad: int) -> bool:
        """Verifica si hay stock suficiente para una cantidad solicitada.

        Args:
            cantidad: Cantidad de unidades solicitadas.

        Returns:
            True si el producto está activo y tiene stock suficiente.
        """
        return self.esta_activo() and self.stock_actual >= cantidad

    def descontar_stock(self, cantidad: int):
        """Descuenta stock del producto tras una venta confirmada.

        Args:
            cantidad: Cantidad de unidades a descontar.

        Raises:
            StockInsuficienteError: Si no hay stock suficiente o el
                producto no está activo.
        """
        if not self.hay_stock_suficiente(cantidad):
            raise StockInsuficienteError(
                self.id, self.nombre, self.stock_actual, cantidad
            )
        self.stock_actual -= cantidad