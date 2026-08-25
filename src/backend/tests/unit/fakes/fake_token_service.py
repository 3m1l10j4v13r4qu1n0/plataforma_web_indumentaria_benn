from app.domain.ports.i_token_service import ITokenService


class FakeTokenService(ITokenService):
    """Fake del servicio de tokens para tests unitarios.

    Genera tokens ficticios con el user_id codificado en el string.
    No valida expiración; solo simula el comportamiento básico.
    """

    def crear_access_token(self, user_id: str, rol: str) -> str:
        return f"access_{user_id}_{rol}"

    def crear_refresh_token(self, user_id: str) -> str:
        return f"refresh_{user_id}"

    def verificar_access_token(self, token: str) -> dict:
        if not token.startswith("access_"):
            raise ValueError("Token inválido")
        parts = token.split("_")
        return {"sub": parts[1], "rol": parts[2], "type": "access"}

    def verificar_refresh_token(self, token: str) -> dict:
        if not token.startswith("refresh_"):
            raise ValueError("Token inválido")
        parts = token.split("_")
        return {"sub": parts[1], "type": "refresh"}
