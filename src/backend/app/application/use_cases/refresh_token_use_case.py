from app.domain.exceptions import TokenInvalidoError
from app.domain.ports.i_token_service import ITokenService
from app.application.use_cases.login_use_case import TokenResponse


class RefreshTokenUseCase:
    """Caso de uso para renovar un access token a partir de un refresh token válido."""

    def __init__(self, token_service: ITokenService):
        self._token_service = token_service

    async def execute(self, refresh_token: str) -> TokenResponse:
        """Verifica el refresh token y genera un nuevo access token.

        Args:
            refresh_token: Token de refresco emitido previamente.

        Returns:
            TokenResponse con el nuevo access token.

        Raises:
            TokenInvalidoError: Si el refresh token es inválido o expiró.
        """
        try:
            payload = self._token_service.verificar_refresh_token(refresh_token)
        except Exception as exc:
            raise TokenInvalidoError() from exc

        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise TokenInvalidoError("Refresh token no contiene 'sub'.")

        nuevo_access = self._token_service.crear_access_token(
            user_id=user_id, rol=payload.get("rol", "")
        )

        return TokenResponse(
            access_token=nuevo_access,
            refresh_token=refresh_token,
        )
