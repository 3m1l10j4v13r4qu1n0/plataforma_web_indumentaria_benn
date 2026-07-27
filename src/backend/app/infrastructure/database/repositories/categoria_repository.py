from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions import CategoriaNoEncontradaError
from app.domain.models.categoria import Categoria
from app.infrastructure.database.orm_models.categoria_orm import CategoriaORM


class CategoriaRepository:
    """
    Implementación concreta de ICategoriaRepository usando SQLAlchemy AsyncSession.
    Nota: el Protocol de dominio no impone async (Paso 1), pero esta
    implementación sí lo es porque el resto de la infraestructura del
    proyecto usa AsyncSession.
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def obtener_por_id(self, categoria_id: int) -> Categoria:
        resultado = await self._session.execute(
            select(CategoriaORM).where(CategoriaORM.id == categoria_id)
        )
        categoria_orm = resultado.scalar_one_or_none()

        if categoria_orm is None:
            raise CategoriaNoEncontradaError(categoria_id)

        return self._mapear_a_dominio(categoria_orm)

    async def listar_todas(self) -> list[Categoria]:
        resultado = await self._session.execute(select(CategoriaORM))
        categorias_orm = resultado.scalars().all()

        return [self._mapear_a_dominio(c) for c in categorias_orm]

    def _mapear_a_dominio(self, categoria_orm: CategoriaORM) -> Categoria:
        return Categoria(
            id=categoria_orm.id,
            nombre=categoria_orm.nombre,
        )