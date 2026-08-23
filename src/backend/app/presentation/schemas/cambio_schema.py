from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ItemVentaTicketResponse(BaseModel):
    producto_id: str
    cantidad: int


class ConsultarVentaPorTicketResponse(BaseModel):
    numero_ticket: str
    fecha_compra: datetime
    dias_transcurridos: int
    es_elegible_para_cambio: bool
    items: list[ItemVentaTicketResponse]

    model_config = ConfigDict(from_attributes=True)


class ProcesarCambioRequest(BaseModel):
    venta_original_id: str = Field(..., description="ID de la venta original")
    cajero_id: str = Field(..., description="ID del cajero que procesa el cambio")
    producto_a_cambiar_id: str = Field(..., description="ID del producto a cambiar")
    nuevo_producto_id: str = Field(
        ..., description="ID del nuevo producto de reemplazo"
    )
    motivo: Optional[str] = Field(None, description="Razón del cambio (opcional)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "venta_original_id": "V-999",
                "cajero_id": "C-005",
                "producto_a_cambiar_id": "123",
                "nuevo_producto_id": "124",
                "motivo": "Talla incorrecta",
            }
        }
    )


class CambioResponse(BaseModel):
    id: str
    venta_original_id: str
    fecha_cambio: datetime
    cajero_id: str
    producto_a_cambiar_id: str
    nuevo_producto_id: str
    estado: str
    motivo: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CambioErrorResponse(BaseModel):
    error: str
    mensaje: str
