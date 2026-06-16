from datetime import datetime
from typing import List, Optional

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
    items: List[ItemVentaRequest] = Field(
        ..., min_length=1, description="Lista de productos a vender"
    )
    porcentaje_descuento: float = Field(
        default=0.0, ge=0.0, le=100.0, description="Porcentaje de descuento aplicado"
    )
    gerente_autorizacion_id: Optional[str] = Field(
        default=None,
        description="ID del gerente que autoriza si el descuento supera el 20%",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "vendedor_id": "V-001",
                "items": [{"producto_id": "123", "cantidad": 2}],
                "porcentaje_descuento": 10.0,
                "gerente_autorizacion_id": None,
            }
        }
    )


class ItemVentaResponse(BaseModel):
    producto_id: str
    cantidad: int


class DescuentoResponse(BaseModel):
    porcentaje: float
    gerente_autorizacion_id: Optional[str] = None


class VentaResponse(BaseModel):
    id: str
    numero_ticket: str = Field(
        ..., description="Número de comprobante único generado para esta venta (HU-07)"
    )  # <-- NUEVO
    fecha_hora: datetime
    vendedor_id: str
    estado: str
    items: List[ItemVentaResponse]
    descuento: DescuentoResponse

    model_config = ConfigDict(from_attributes=True)


class StockResponse(BaseModel):
    producto_id: str
    nombre: str
    stock_actual: int


class ErrorResponse(BaseModel):
    error: str
    mensaje: str
    producto_id: str | None = None
    usuario_id: str | None = None
