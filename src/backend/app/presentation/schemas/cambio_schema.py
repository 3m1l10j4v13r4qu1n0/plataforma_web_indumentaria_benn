# Definimos los DTOs de entrada y salida para la validación de elegibilidad de cambio.

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SolicitarCambioRequest(BaseModel):
    numero_ticket: str = Field(
        ..., description="Número de comprobante de la compra original"
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"numero_ticket": "TKT-20231025-001"}}
    )


class ElegibilidadCambioResponse(BaseModel):
    venta_id: str
    numero_ticket: str
    fecha_compra: datetime
    estado: str
    mensaje: str

    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    error: str
    mensaje: str
    numero_ticket: str | None = None
