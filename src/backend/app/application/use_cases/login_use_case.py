from dataclasses import dataclass

from app.domain.exceptions import CredencialesInvalidasError
from app.domain.ports.i_password_hasher import IPasswordHasher
from app.domain.ports.i_token_service import ITokenService
from app.domain.ports.i_usuario_repository import IUsuarioRepository
from app.infrastructure.core.config import settings


@dataclass
class TokenResponse:
    """DTO de salida con los tokens generados tras un login exitoso."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60


class LoginUseCase:
    """Caso de uso para autenticar un usuario y emitir tokens JWT.

    Valida credenciales, genera access token y refresh token.
    """

    def __init__(
        self,
        usuario_repository: IUsuarioRepository,
        password_hasher: IPasswordHasher,
        token_service: ITokenService,
    ):
        self._usuario_repository = usuario_repository
        self._password_hasher = password_hasher
        self._token_service = token_service

    async def execute(self, email: str, password: str) -> TokenResponse:
        """Autentica un usuario y retorna tokens de acceso.

        Args:
            email: Email del usuario.
            password: Contraseña en texto plano.

        Returns:
            TokenResponse con access y refresh token.

        Raises:
            CredencialesInvalidasError: Si el email no existe o la
                contraseña no coincide.
        """
        usuario = await self._usuario_repository.buscar_por_email(email)

        if usuario is None or not self._password_hasher.verify(
            password, usuario.password_hash
        ):
            raise CredencialesInvalidasError()

        access_token = self._token_service.crear_access_token(
            user_id=usuario.id, rol=usuario.rol.value
        )
        refresh_token = self._token_service.crear_refresh_token(
            user_id=usuario.id
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
