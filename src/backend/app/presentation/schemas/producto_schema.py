from typing import List

from pydantic import BaseModel, ConfigDict, Field


class ProductoStockResumenSchema(BaseModel):
    producto_id: str = Field(..., description="Identificador único del producto")
    codigo: str = Field(..., description="Código de barras o SKU")
    nombre: str = Field(..., description="Nombre descriptivo del producto")
    stock_actual: int = Field(
        ..., ge=0, description="Cantidad disponible en inventario"
    )
    estado: str = Field(..., description="Estado del producto (ACTIVO o INACTIVO)")

    model_config = ConfigDict(from_attributes=True)


class BuscarProductosResponseSchema(BaseModel):
    productos: List[ProductoStockResumenSchema] = Field(
        ..., description="Lista de productos encontrados"
    )
    mensaje: str = Field(
        ..., description="Mensaje contextual sobre el resultado de la búsqueda"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "productos": [
                    {
                        "producto_id": "123e4567-e89b-12d3-a456-426614174000",
                        "codigo": "CAM-001",
                        "nombre": "Camiseta Básica",
                        "stock_actual": 5,
                        "estado": "ACTIVO",
                    }
                ],
                "mensaje": "Se encontraron 1 producto(s).",
            }
        }
    )
