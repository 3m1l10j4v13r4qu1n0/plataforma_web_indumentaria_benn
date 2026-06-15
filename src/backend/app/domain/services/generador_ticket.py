import uuid
from datetime import datetime


def generar_numero_ticket() -> str:
    """
    Genera un número de ticket único con formato legible.
    Formato: TKT-YYYYMMDD-XXXXXX (ej: TKT-20231025-A1B2C3)

    Nota: Al usar uuid4().hex[:6], la probabilidad de colisión es
    extremadamente baja para el volumen de un retail, cumpliendo con KISS.
    Si el negocio requiere secuenciales estrictos (ej: 000001),
    esto se implementaría vía un Puerto (ISequentialGenerator) en la infraestructura.
    """
    fecha = datetime.utcnow().strftime("%Y%m%d")
    sufijo_unico = uuid.uuid4().hex[:6].upper()
    return f"TKT-{fecha}-{sufijo_unico}"
