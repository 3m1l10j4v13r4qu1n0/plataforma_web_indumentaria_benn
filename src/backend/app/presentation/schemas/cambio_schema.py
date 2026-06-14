from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ItemCambioRequest(BaseModel):
    producto_id: str = Field(..., description="ID del producto que se desea cambiar")
    condicion_declarada: str = Field(
        ..., description="Condición del producto: debe ser 'NUEVO_CON_ETIQUETA'"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "producto_id": "P-001",
                "condicion_declarada": "NUEVO_CON_ETIQUETA",
            }
        }
    )


class SolicitarCambioRequest(BaseModel):
    numero_ticket: str = Field(
        ..., description="Número de comprobante de la compra original"
    )
    items_a_cambiar: List[ItemCambioRequest] = Field(
        ...,
        min_length=1,
        description="Lista de productos del ticket que se desean cambiar",
    )


class ItemCambioValidadoResponse(BaseModel):
    producto_id: str
    nombre: str
    cantidad_original: int
    condicion_validada: str


class ElegibilidadCambioResponse(BaseModel):
    venta_id: str
    numero_ticket: str
    fecha_compra: datetime
    estado: str
    items_validados: List[ItemCambioValidadoResponse]
    mensaje: str

    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    error: str
    mensaje: str
    numero_ticket: str | None = None
    producto_id: str | None = None
