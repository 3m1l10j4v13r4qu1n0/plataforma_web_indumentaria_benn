from dataclasses import dataclass

@dataclass
class ProductoStockResumenDTO:
    producto_id: str
    codigo: str
    nombre: str
    categoria_id: int
    precio: int
    stock_actual: int
    estado: str

@dataclass
class BuscarProductosResponseDTO:
    productos: list[ProductoStockResumenDTO]
    mensaje: str