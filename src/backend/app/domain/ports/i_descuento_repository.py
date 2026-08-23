from typing import Protocol

from app.domain.models.descuento import Descuento


class IDescuentoRepository(Protocol):
    """Puerto para la persistencia de descuentos."""

    async def crear_descuento(self, descuento: Descuento) -> Descuento:
        """Registra un nuevo descuento en el sistema.

        Args:
            descuento: La entidad de descuento a persistir.

        Returns:
            El descuento persistido con los datos actualizados.
        """
        ...

    async def obtener_por_venta_id(self, venta_id: str) -> Descuento | None:
        """Obtiene el descuento asociado a una venta específica.

        Args:
            venta_id: ID de la venta.

        Returns:
            El descuento si existe, None caso contrario.
        """
        ...

    async def obtener_por_id(self, descuento_id: str) -> Descuento | None:
        """Obtiene un descuento por su ID.

        Args:
            descuento_id: ID único del descuento.

        Returns:
            El descuento si existe, None caso contrario.
        """
        ...
