from typing import Optional

from app.domain.models.usuario import RolUsuario, Usuario


class FakeUsuarioRepository:
    """Fake del repositorio de usuarios para tests unitarios (sin DB)."""

    def __init__(self) -> None:
        self._usuarios: dict[str, Usuario] = {}
        self._por_email: dict[str, Usuario] = {}

    async def buscar_por_email(self, email: str) -> Optional[Usuario]:
        return self._por_email.get(email)

    async def crear(self, usuario: Usuario) -> Usuario:
        self._usuarios[usuario.id] = usuario
        self._por_email[usuario.email] = usuario
        return usuario

    def agregar_usuario(self, usuario: Usuario) -> None:
        """Método auxiliar para precargar datos en el arrange de tests."""
        self._usuarios[usuario.id] = usuario
        self._por_email[usuario.email] = usuario
