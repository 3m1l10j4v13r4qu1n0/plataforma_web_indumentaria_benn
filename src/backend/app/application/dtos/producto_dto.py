from dataclasses import dataclass
from typing import List


@dataclass
class BuscarProductosCommand:
    query: str  # Término de búsqueda (código exacto o fragmento de nombre)


@dataclass
class ProductoStockResumenDTO:
    """
    Definimos aquí el DTO que el Caso de Uso devolverá,
    para no exponer la entidad de dominio completa
    (que podría tener campos internos) en la capa de
    presentación, cumpliendo con el principio de
    bajo acoplamiento.
    """

    producto_id: str
    codigo: str
    nombre: str
    stock_actual: int
    estado: str


@dataclass
class BuscarProductosResponseDTO:
    productos: List[ProductoStockResumenDTO]
    mensaje: str
