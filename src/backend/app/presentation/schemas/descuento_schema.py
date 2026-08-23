from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AplicarDescuentoRequest(BaseModel):
    """Schema de entrada para aplicar un descuento a una venta."""

    venta_id: str = Field(..., description="ID de la venta a la que se aplica el descuento")
    porcentaje: Decimal = Field(
        ...,
        gt=0,
        le=100,
        description="Porcentaje de descuento (0-100)",
    )
    motivo: str = Field(
        ...,
        min_length=5,
        max_length=255,
        description="Motivo del descuento",
    )
    autorizado_por: str | None = Field(
        None,
        description="ID del gerente que autoriza (requerido si el descuento supera el 20%)",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "venta_id": "V-001",
                "porcentaje": 15.0,
                "motivo": "Promoción de temporada",
                "autorizado_por": None,
            }
        }
    )


class DescuentoResponse(BaseModel):
    """Schema de salida con los datos del descuento registrado."""

    id: str
    venta_id: str
    porcentaje: Decimal
    monto_descuento: Decimal
    motivo: str
    autorizado_por: str | None = None
    fecha_aplicacion: datetime | None = None
    requiere_autorizacion: bool = Field(
        ...,
        description="Indica si el descuento requería autorización",
    )
    mensaje: str | None = None

    model_config = ConfigDict(from_attributes=True)
