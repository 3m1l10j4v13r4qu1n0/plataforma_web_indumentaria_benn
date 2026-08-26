"""Script para crear un usuario GERENTE inicial en la base de datos.

Ejecutar desde src/backend/:
    python -m scripts.seed_admin

Credenciales hardcodeadas:
    Email: admin@benn.com
    Password: admin123
    Rol: GERENTE
"""

import asyncio
import uuid

from sqlalchemy import select

from app.domain.models.usuario import RolUsuario
from app.infrastructure.auth.bcrypt_password_hasher import BcryptPasswordHasher
from app.infrastructure.database.orm_models.usuario_orm import UsuarioORM
from app.infrastructure.database.session import AsyncSessionLocal

EMAIL_ADMIN = "admin@benn.com"
PASSWORD_ADMIN = "admin123"
NOMBRE_ADMIN = "Administrador"


async def seed_admin() -> None:
    """Crea el usuario GERENTE si no existe."""
    hasher = BcryptPasswordHasher()

    async with AsyncSessionLocal() as session:
        stmt = select(UsuarioORM).where(UsuarioORM.email == EMAIL_ADMIN)
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            print(f"El usuario {EMAIL_ADMIN} ya existe. No se crea duplicado.")
            return

        admin_user = UsuarioORM(
            id=str(uuid.uuid4()),
            email=EMAIL_ADMIN,
            password_hash=hasher.hash(PASSWORD_ADMIN),
            nombre=NOMBRE_ADMIN,
            rol=RolUsuario.GERENTE.value,
            activo=True,
        )
        session.add(admin_user)
        await session.commit()
        print(f"Usuario GERENTE creado: {EMAIL_ADMIN} / {PASSWORD_ADMIN}")


if __name__ == "__main__":
    asyncio.run(seed_admin())
