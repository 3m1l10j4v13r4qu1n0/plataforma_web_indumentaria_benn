from dataclasses import dataclass
from datetime import datetime


@dataclass
class SolicitarCambioCommand:
    """
    Definimos un comando simple para encapsular
    los datos de entrada necesarios para
    solicitar/validar un cambio.

    """

    numero_ticket: str
    fecha_solicitud: datetime
    # Normalmente será datetime.utcnow() desde el router
