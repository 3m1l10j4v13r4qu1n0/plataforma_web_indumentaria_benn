from dataclasses import dataclass
from enum import Enum


class RolUsuario(str, Enum):
    """Roles disponibles en el sistema SGVIR."""

    VENDEDOR = "VENDEDOR"
    CAJERO = "CAJERO"
    GERENTE = "GERENTE"
    ENCARGADO_VENTAS = "ENCARGADO_VENTAS"


@dataclass
class Usuario:
    """Entidad de dominio que representa un usuario del sistema."""

    id: str
    email: str
    password_hash: str
    nombre: str
    rol: RolUsuario
    activo: bool = True

    def esta_activo(self) -> bool:
        """Verifica si el usuario está habilitado en el sistema."""
        return self.activo

    def tiene_rol(self, rol: RolUsuario) -> bool:
        """Verifica si el usuario tiene el rol indicado."""
        return self.rol == rol
