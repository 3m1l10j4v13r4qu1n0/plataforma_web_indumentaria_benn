from typing import Optional, Protocol

from app.domain.models.venta import Venta


class IVentaRepository(Protocol):
    """
    Actualización del Puerto: IVentaRepository
    (app/domain/ports/i_venta_repository.py)
    Necesitamos poder buscar una venta por su número
    de ticket para validar el cambio, ya que el actor
    (Cajero) recibirá el comprobante físico o digital
    del cliente.
    """

    async def crear_venta(self, venta: Venta) -> Venta: ...

    async def obtener_por_numero_ticket(self, numero_ticket: str) -> Optional[Venta]:
        """
        Recupera una venta utilizando su número de comprobante único.
        """
        ...
