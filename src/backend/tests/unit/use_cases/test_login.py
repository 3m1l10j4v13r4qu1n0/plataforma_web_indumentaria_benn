import pytest

from app.application.use_cases.login_use_case import LoginUseCase
from app.domain.exceptions import CredencialesInvalidasError
from app.domain.models.usuario import RolUsuario, Usuario
from tests.unit.fakes.fake_password_hasher import FakePasswordHasher
from tests.unit.fakes.fake_token_service import FakeTokenService
from tests.unit.fakes.fake_usuario_repository import FakeUsuarioRepository


@pytest.fixture
def usuario_repo():
    return FakeUsuarioRepository()


@pytest.fixture
def password_hasher():
    return FakePasswordHasher()


@pytest.fixture
def token_service():
    return FakeTokenService()


@pytest.fixture
def use_case(usuario_repo, password_hasher, token_service):
    return LoginUseCase(
        usuario_repository=usuario_repo,
        password_hasher=password_hasher,
        token_service=token_service,
    )


@pytest.fixture
def usuario_activo():
    return Usuario(
        id="USER-001",
        email="activo@test.com",
        password_hash="hashed_mipassword",
        nombre="Usuario Activo",
        rol=RolUsuario.CAJERO,
        activo=True,
    )


@pytest.fixture
def usuario_inactivo():
    return Usuario(
        id="USER-002",
        email="inactivo@test.com",
        password_hash="hashed_pass",
        nombre="Usuario Inactivo",
        rol=RolUsuario.VENDEDOR,
        activo=False,
    )


# ── Escenario 1: Login exitoso ───────────────────────────────────────
@pytest.mark.asyncio
async def test_login_exitoso(use_case, usuario_repo, usuario_activo):
    # Arrange
    usuario_repo.agregar_usuario(usuario_activo)

    # Act
    resultado = await use_case.execute("activo@test.com", "mipassword")

    # Assert
    assert resultado is not None
    assert resultado.access_token == "access_USER-001_CAJERO"
    assert resultado.refresh_token == "refresh_USER-001"
    assert resultado.token_type == "bearer"
    assert resultado.expires_in > 0


# ── Escenario 2: Email no existe ─────────────────────────────────────
@pytest.mark.asyncio
async def test_email_no_existente_lanza_excepcion(use_case):
    # Act & Assert
    with pytest.raises(CredencialesInvalidasError):
        await use_case.execute("noexiste@test.com", "password")


# ── Escenario 3: Password incorrecta ────────────────────────────────
@pytest.mark.asyncio
async def test_password_incorrecta_lanza_excepcion(
    use_case, usuario_repo, usuario_activo
):
    # Arrange
    usuario_repo.agregar_usuario(usuario_activo)

    # Act & Assert
    with pytest.raises(CredencialesInvalidasError):
        await use_case.execute("activo@test.com", "password_incorrecta")


# ── Escenario 4: Usuario inactivo ───────────────────────────────────
@pytest.mark.asyncio
async def test_usuario_inactivo_login_exitoso(
    use_case, usuario_repo, usuario_inactivo
):
    # Arrange - El login no valida si el usuario está activo;
    # esa validación se hace en get_current_user al verificar el token.
    usuario_repo.agregar_usuario(usuario_inactivo)

    # Act
    resultado = await use_case.execute("inactivo@test.com", "pass")

    # Assert - El use case genera tokens igualmente
    assert resultado is not None
    assert resultado.access_token.startswith("access_")


# ── Escenario 5: Tokens generados correctamente ─────────────────────
@pytest.mark.asyncio
async def test_tokens_contienen_datos_usuario(
    use_case, usuario_repo, usuario_activo
):
    # Arrange
    usuario_repo.agregar_usuario(usuario_activo)

    # Act
    resultado = await use_case.execute("activo@test.com", "mipassword")

    # Assert
    assert "USER-001" in resultado.access_token
    assert "USER-001" in resultado.refresh_token
    assert "CAJERO" in resultado.access_token
