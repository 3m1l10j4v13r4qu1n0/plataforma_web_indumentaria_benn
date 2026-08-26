from pydantic import BaseModel


class ResumenDashboard(BaseModel):
    """DTO de respuesta del dashboard principal."""

    ventas_hoy: int
    total_facturado_hoy: float
    productos_stock_bajo: int


class ProductoStockBajo(BaseModel):
    """Producto con stock por debajo del umbral."""

    producto_id: str
    codigo: str
    nombre: str
    stock_actual: int
