from pydantic import BaseModel, Field


class ProductoStockResponse(BaseModel):
    """Producto resultante de una búsqueda, con su stock actual."""

    producto_id: str = Field(..., description="ID único del producto")
    codigo: str = Field(..., description="Código de barras o SKU del producto")
    nombre: str = Field(..., description="Nombre descriptivo del producto")
    stock_actual: int = Field(
        ..., ge=0, description="Cantidad disponible en inventario"
    )
    estado: str = Field(..., description="Estado del producto (ej. ACTIVO)")


class BuscarProductosResponse(BaseModel):
    """Respuesta de la búsqueda de productos por nombre o código."""

    resultados: list[ProductoStockResponse] = Field(
        ..., description="Productos activos que coinciden con la búsqueda"
    )
    total_encontrados: int = Field(
        ..., ge=0, description="Cantidad total de productos encontrados"
    )
    mensaje: str | None = Field(
        default=None,
        description="Mensaje informativo cuando la búsqueda no arroja resultados",
    )
