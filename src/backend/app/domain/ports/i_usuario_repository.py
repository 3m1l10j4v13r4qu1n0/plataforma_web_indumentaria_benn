from typing import Protocol

from app.domain.models.usuario import Usuario


class IUsuarioRepository(Protocol):
    """Puerto de salida para la persistencia de usuarios."""

    async def buscar_por_email(self, email: str) -> Usuario | None: ...

    async def crear(self, usuario: Usuario) -> Usuario: ...
