from app.domain.ports.i_password_hasher import IPasswordHasher


class FakePasswordHasher(IPasswordHasher):
    """Fake del hasher de contraseñas para tests unitarios.

    No usa bcrypt real; simplemente agrega un prefijo para simular el hash.
    """

    def hash(self, password: str) -> str:
        return f"hashed_{password}"

    def verify(self, password: str, hashed: str) -> bool:
        return hashed == f"hashed_{password}"
