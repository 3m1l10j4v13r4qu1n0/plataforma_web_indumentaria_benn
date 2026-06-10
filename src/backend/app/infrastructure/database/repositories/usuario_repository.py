# HU-05
from app.domain.ports.i_usuario_repository import IUsuarioRepository
from app.infrastructure.database.orm_models.usuario_orm import UsuarioORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UsuarioRepository(IUsuarioRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def es_gerente(self, usuario_id: str) -> bool:
        """
        Verifica si el usuario tiene el rol de GERENTE.
        """
        stmt = select(UsuarioORM).where(UsuarioORM.id == usuario_id)
        result = await self.session.execute(stmt)
        usuario = result.scalar_one_or_none()

        if not usuario:
            return False

        return usuario.rol.upper() == "GERENTE"
