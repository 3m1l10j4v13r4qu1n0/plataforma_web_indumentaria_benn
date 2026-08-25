from typing import Protocol


class IPasswordHasher(Protocol):
    """Puerto de salida para el hashing de contraseñas."""

    def hash(self, password: str) -> str: ...

    def verify(self, password: str, hashed: str) -> bool: ...
