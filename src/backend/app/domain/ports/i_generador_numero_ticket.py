from typing import Protocol


class IGeneradorNumeroTicket(Protocol):
    """Puerto para la generación automática de números de ticket únicos.

    La secuencia y la fecha son dependencias externas (reloj, BD), por lo que
    se abstraen detrás de este contrato e implementan en infraestructura.
    """

    async def generar(self) -> str:
        """Genera un número de ticket único para una venta confirmada.

        Returns:
            El número de ticket con formato T-YYYYMMDD-NNN.
        """
        ...
