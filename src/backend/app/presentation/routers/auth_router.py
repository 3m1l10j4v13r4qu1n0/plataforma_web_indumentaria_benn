from app.application.use_cases.login_use_case import LoginUseCase
from app.application.use_cases.refresh_token_use_case import RefreshTokenUseCase
from app.application.use_cases.registrar_usuario_use_case import (
    RegistrarUsuarioUseCase,
)
from app.domain.models.usuario import RolUsuario
from app.infrastructure.dependencies.dependency_injection import (
    get_login_use_case,
    get_refresh_token_use_case,
    get_registrar_usuario_use_case,
)
from app.presentation.dependencies import RequireRole
from app.presentation.schemas.auth_schema import (
    LoginRequest,
    RefreshRequest,
    RegistroRequest,
    TokenResponse,
    UsuarioResponse,
)
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])


@router.post(
    "/registro",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario nuevo",
    dependencies=[Depends(RequireRole(RolUsuario.GERENTE))],
)
async def registrar_usuario(
    request: RegistroRequest,
    use_case: RegistrarUsuarioUseCase = Depends(get_registrar_usuario_use_case),
):
    """
    Registra un usuario nuevo en el sistema.
    El email debe ser único. La contraseña tiene mínimo 6 caracteres.
    """
    rol = RolUsuario(request.rol)
    usuario = await use_case.execute(
        email=request.email,
        password=request.password,
        nombre=request.nombre,
        rol=rol,
    )

    return UsuarioResponse(
        id=usuario.id,
        email=usuario.email,
        nombre=usuario.nombre,
        rol=usuario.rol.value,
        activo=usuario.activo,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión",
)
async def login(
    request: LoginRequest,
    use_case: LoginUseCase = Depends(get_login_use_case),
):
    """
    Autentica un usuario con email y contraseña.
    Devuelve access token (15 min) y refresh token (7 días).
    """
    resultado = await use_case.execute(
        email=request.email,
        password=request.password,
    )

    return TokenResponse(
        access_token=resultado.access_token,
        refresh_token=resultado.refresh_token,
        token_type=resultado.token_type,
        expires_in=resultado.expires_in,
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Renovar access token",
)
async def refresh_token(
    request: RefreshRequest,
    use_case: RefreshTokenUseCase = Depends(get_refresh_token_use_case),
):
    """
    Renueva el access token usando un refresh token válido.
    El refresh token se mantiene sin cambios.
    """
    resultado = await use_case.execute(refresh_token=request.refresh_token)

    return TokenResponse(
        access_token=resultado.access_token,
        refresh_token=resultado.refresh_token,
        token_type=resultado.token_type,
        expires_in=resultado.expires_in,
    )
