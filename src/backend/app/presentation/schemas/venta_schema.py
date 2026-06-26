from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemVentaRequest(BaseModel):
    producto_id: str = Field(..., description="ID único del producto")
    cantidad: int = Field(
        ..., gt=0, description="Cantidad a vender, debe ser mayor a 0"
    )


class CrearVentaRequest(BaseModel):
    vendedor_id: str = Field(
        ..., description="ID del vendedor que realiza la operación"
    )
    items: list[ItemVentaRequest] = Field(
        ..., min_length=1, description="Lista de productos a vender"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "vendedor_id": "V-001",
                "items": [{"producto_id": "123", "cantidad": 2}],
            }
        }
    )


class ItemVentaResponse(BaseModel):
    producto_id: str
    cantidad: int


class VentaResponse(BaseModel):
    id: str
    fecha_hora: datetime
    vendedor_id: str
    estado: str
    items: list[ItemVentaResponse]

    model_config = ConfigDict(from_attributes=True)


class StockResponse(BaseModel):
    producto_id: str
    nombre: str
    stock_actual: int


class ErrorResponse(BaseModel):
    error: str
    mensaje: str
    producto_id: str | None = None
