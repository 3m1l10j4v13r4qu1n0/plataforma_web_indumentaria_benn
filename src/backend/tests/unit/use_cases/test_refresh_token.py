import pytest

from app.application.use_cases.refresh_token_use_case import RefreshTokenUseCase
from app.domain.exceptions import TokenInvalidoError
from tests.unit.fakes.fake_token_service import FakeTokenService


@pytest.fixture
def token_service():
    return FakeTokenService()


@pytest.fixture
def use_case(token_service):
    return RefreshTokenUseCase(token_service=token_service)


# ── Escenario 1: Refresh exitoso ─────────────────────────────────────
@pytest.mark.asyncio
async def test_refresh_exitoso(use_case):
    # Arrange
    refresh_token = "refresh_USER-001"

    # Act
    resultado = await use_case.execute(refresh_token)

    # Assert
    assert resultado is not None
    assert resultado.access_token == "access_USER-001_"
    assert resultado.refresh_token == refresh_token
    assert resultado.token_type == "bearer"
    assert resultado.expires_in > 0


# ── Escenario 2: Token inválido ─────────────────────────────────────
@pytest.mark.asyncio
async def test_token_invalido_lanza_excepcion(use_case):
    # Arrange
    token_invalido = "token_invalido"

    # Act & Assert
    with pytest.raises(TokenInvalidoError):
        await use_case.execute(token_invalido)


# ── Escenario 3: Refresh token mantiene el mismo token ──────────────
@pytest.mark.asyncio
async def test_refresh_mantiene_mismo_token(use_case):
    # Arrange
    refresh_token = "refresh_USER-002"

    # Act
    resultado = await use_case.execute(refresh_token)

    # Assert
    assert resultado.refresh_token == refresh_token


# ── Escenario 4: Nuevo access token tiene datos del usuario ─────────
@pytest.mark.asyncio
async def test_nuevo_access_token_contiene_user_id(use_case):
    # Arrange
    refresh_token = "refresh_USER-003"

    # Act
    resultado = await use_case.execute(refresh_token)

    # Assert
    assert "USER-003" in resultado.access_token
    assert resultado.access_token.startswith("access_")
