# HU-05 Implementacion de descuento
from dataclasses import dataclass
from typing import Optional

from app.domain.exceptions import DescuentoExcedeLimiteError

# Constante de dominio (podría moverse a un settings de dominio si varía por configuración)
MAX_DESCUENTO_SIN_AUTORIZACION = 20.0  # 20%


@dataclass(frozen=True)  # frozen=True garantiza que sea inmutable (Value Object)
class Descuento:
    porcentaje: float = 0.0
    gerente_autorizacion_id: Optional[str] = None

    def __post_init__(self):
        # Responsabilidad 1: Validar rango matemático
        if self.porcentaje < 0.0 or self.porcentaje > 100.0:
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100.")

        # Responsabilidad 2: Validar regla de negocio transversal de autorización
        if self.porcentaje > MAX_DESCUENTO_SIN_AUTORIZACION:
            if not self.gerente_autorizacion_id:
                raise DescuentoExcedeLimiteError(
                    porcentaje_solicitado=self.porcentaje,
                    limite_permitido=MAX_DESCUENTO_SIN_AUTORIZACION,
                )
