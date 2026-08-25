from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.domain.exceptions import (
    TokenInvalidoError,
    UsuarioNoAutorizadoError,
    UsuarioNoAutenticadoError,
)
from app.domain.models.usuario import RolUsuario, Usuario
from app.infrastructure.auth.jwt_token_service import JWTTokenService
from app.infrastructure.database.repositories.usuario_repository import (
    UsuarioRepository,
)
from app.infrastructure.dependencies.dependency_injection import (
    get_token_service,
    get_usuario_repository,
)

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    token_service: JWTTokenService = Depends(get_token_service),
    usuario_repository: UsuarioRepository = Depends(get_usuario_repository),
) -> Usuario:
    """Extrae y valida el access token del header Authorization.

    Retorna la entidad Usuario si el token es válido y el usuario existe
    y está activo.

    Raises:
        UsuarioNoAutenticadoError: Si no se provee token.
        TokenInvalidoError: Si el token es inválido o expiró.
        UsuarioNoAutenticadoError: Si el usuario no existe o está inactivo.
    """
    token = credentials.credentials

    try:
        payload = token_service.verificar_access_token(token)
    except Exception as exc:
        raise TokenInvalidoError() from exc

    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise TokenInvalidoError("Token no contiene 'sub'.")

    usuario = await usuario_repository.buscar_por_email(user_id)
    if usuario is None:
        raise UsuarioNoAutenticadoError()

    if not usuario.esta_activo():
        raise UsuarioNoAutenticadoError()

    return usuario


class RequireRole:
    """Dependency factory que valida que el usuario tenga un rol específico.

    Uso:
        @router.get("/admin", dependencies=[Depends(RequireRole(Role.GERENTE))])
    """

    def __init__(self, rol_requerido: RolUsuario):
        self.rol_requerido = rol_requerido

    async def __call__(
        self, usuario: Annotated[Usuario, Depends(get_current_user)]
    ) -> Usuario:
        if not usuario.tiene_rol(self.rol_requerido):
            raise UsuarioNoAutorizadoError(self.rol_requerido.value)
        return usuario
