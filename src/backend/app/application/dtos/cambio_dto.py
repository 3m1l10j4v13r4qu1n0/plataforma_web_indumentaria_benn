"""
Para que el Caso de Uso pueda evaluar la condición, necesitamos que el comando
de solicitud incluya el ID del producto que se desea cambiar y su condición
declarada por el cajero/vendedor.

"""

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class ItemCambioDTO:
    producto_id: str
    condicion_declarada: str  # Ej: "NUEVO_CON_ETIQUETA", "USADO", "SIN_ETIQUETA"


@dataclass
class SolicitarCambioCommand:
    numero_ticket: str
    fecha_solicitud: datetime
    items_a_cambiar: List[
        ItemCambioDTO
    ]  # Nuevo: Ahora podemos validar múltiples productos del mismo ticket
