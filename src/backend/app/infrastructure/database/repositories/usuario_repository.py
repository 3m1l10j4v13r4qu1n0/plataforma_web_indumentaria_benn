from typing import Optional

from app.domain.models.usuario import RolUsuario, Usuario
from app.domain.ports.i_usuario_repository import IUsuarioRepository
from app.infrastructure.database.orm_models.usuario_orm import UsuarioORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UsuarioRepository(IUsuarioRepository):
    """Implementación concreta del repositorio de usuarios sobre PostgreSQL."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def buscar_por_email(self, email: str) -> Optional[Usuario]:
        stmt = select(UsuarioORM).where(UsuarioORM.email == email)
        result = await self.session.execute(stmt)
        orm_usuario = result.scalar_one_or_none()

        if not orm_usuario:
            return None

        return Usuario(
            id=orm_usuario.id,
            email=orm_usuario.email,
            password_hash=orm_usuario.password_hash,
            nombre=orm_usuario.nombre,
            rol=RolUsuario(orm_usuario.rol),
            activo=orm_usuario.activo,
        )

    async def crear(self, usuario: Usuario) -> Usuario:
        orm_usuario = UsuarioORM(
            id=usuario.id,
            email=usuario.email,
            password_hash=usuario.password_hash,
            nombre=usuario.nombre,
            rol=usuario.rol.value,
            activo=usuario.activo,
        )
        self.session.add(orm_usuario)
        await self.session.flush()

        return usuario
