from pydantic import BaseModel, ConfigDict


class ProductoStockResumenDTO(BaseModel):
    """Representa el resumen de stock de un producto para consulta.

    Attributes:
        producto_id: Identificador único del producto (UUID).
        codigo: Código de barras o SKU del producto.
        nombre: Nombre descriptivo del producto.
        categoria_id: Identificador de la categoría del producto.
        precio: Precio unitario del producto.
        stock_actual: Cantidad disponible en inventario.
        estado: Estado actual del producto como string.
    """

    model_config = ConfigDict(from_attributes=True)

    producto_id: str
    codigo: str
    nombre: str
    categoria_id: int
    precio: int
    stock_actual: int
    estado: str


class BuscarProductosResponseDTO(BaseModel):
    """Respuesta de la búsqueda de productos por stock (HU-06).

    Attributes:
        productos: Lista de resúmenes de stock encontrados.
        mensaje: Mensaje descriptivo del resultado de la búsqueda.
    """

    productos: list[ProductoStockResumenDTO]
    mensaje: str