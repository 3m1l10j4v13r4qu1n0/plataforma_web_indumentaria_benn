import bcrypt

from app.domain.ports.i_password_hasher import IPasswordHasher


class BcryptPasswordHasher(IPasswordHasher):
    """Adaptador concreto de hashing de contraseñas usando bcrypt."""

    def hash(self, password: str) -> str:
        """Genera un hash bcrypt de la contraseña.

        Args:
            password: Contraseña en texto plano.

        Returns:
            Hash bcrypt resultante.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify(self, password: str, hashed: str) -> bool:
        """Verifica si una contraseña coincide con su hash.

        Args:
            password: Contraseña en texto plano.
            hashed: Hash almacenado en la base de datos.

        Returns:
            True si la contraseña coincide, False en caso contrario.
        """
        return bcrypt.checkpw(
            password.encode("utf-8"), hashed.encode("utf-8")
        )
