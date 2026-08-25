from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.domain.ports.i_token_service import ITokenService
from app.infrastructure.core.config import settings


class JWTTokenService(ITokenService):
    """Adaptador concreto de servicio de tokens JWT usando python-jose."""

    def crear_access_token(self, user_id: str, rol: str) -> str:
        """Crea un access token con expiración corta.

        Args:
            user_id: ID del usuario.
            rol: Rol del usuario.

        Returns:
            Token JWT firmado.
        """
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {
            "sub": user_id,
            "rol": rol,
            "exp": expire,
            "type": "access",
        }
        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    def crear_refresh_token(self, user_id: str) -> str:
        """Crea un refresh token con expiración larga.

        Args:
            user_id: ID del usuario.

        Returns:
            Token JWT de refresco firmado.
        """
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        payload = {
            "sub": user_id,
            "exp": expire,
            "type": "refresh",
        }
        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    def verificar_access_token(self, token: str) -> dict:
        """Verifica y decodifica un access token.

        Args:
            token: Token JWT a verificar.

        Returns:
            Payload del token decodificado.

        Raises:
            TokenInvalidoError: Si el token es inválido, expirado o no es
                un access token.
        """
        payload = self._verificar_token(token, expected_type="access")
        return payload

    def verificar_refresh_token(self, token: str) -> dict:
        """Verifica y decodifica un refresh token.

        Args:
            token: Token JWT de refresco a verificar.

        Returns:
            Payload del token decodificado.

        Raises:
            TokenInvalidoError: Si el token es inválido, expirado o no es
                un refresh token.
        """
        payload = self._verificar_token(token, expected_type="refresh")
        return payload

    def _verificar_token(self, token: str, expected_type: str) -> dict:
        """Método interno para verificar tokens JWT.

        Args:
            token: Token JWT a verificar.
            expected_type: Tipo esperado ('access' o 'refresh').

        Returns:
            Payload del token decodificado.

        Raises:
            JWTError: Si la verificación falla.
        """
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        token_type = payload.get("type")
        if token_type != expected_type:
            raise JWTError(
                f"Token inválido: se esperaba '{expected_type}', "
                f"se recibió '{token_type}'."
            )
        return payload
