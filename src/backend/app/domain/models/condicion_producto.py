from dataclasses import dataclass

from app.domain.exceptions import ProductoNoAptoParaCambioError


@dataclass(frozen=True)
class CondicionProducto:
    """
    Este objeto representa el estado declarado del producto
    que se desea cambiar. Su única responsabilidad es garantizar
    que cumpla con la regla de negocio inquebrantable.

    """

    estado_declarado: str

    def __post_init__(self):
        # Regla de Negocio Transversal HU-03
        if self.estado_declarado != "NUEVO_CON_ETIQUETA":
            raise ProductoNoAptoParaCambioError(condicion=self.estado_declarado)
