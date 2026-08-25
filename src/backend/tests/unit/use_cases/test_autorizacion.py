import pytest

from app.domain.exceptions import UsuarioNoAutorizadoError
from app.domain.models.usuario import RolUsuario, Usuario
from app.presentation.dependencies import RequireAnyRole, RequireRole


@pytest.fixture
def usuario_vendedor():
    return Usuario(
        id="USER-001",
        email="vendedor@test.com",
        password_hash="hashed_pass",
        nombre="Vendedor Test",
        rol=RolUsuario.VENDEDOR,
        activo=True,
    )


@pytest.fixture
def usuario_cajero():
    return Usuario(
        id="USER-002",
        email="cajero@test.com",
        password_hash="hashed_pass",
        nombre="Cajero Test",
        rol=RolUsuario.CAJERO,
        activo=True,
    )


@pytest.fixture
def usuario_gerente():
    return Usuario(
        id="USER-003",
        email="gerente@test.com",
        password_hash="hashed_pass",
        nombre="Gerente Test",
        rol=RolUsuario.GERENTE,
        activo=True,
    )


# ── RequireRole ─────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_require_role_usuario_con_rol_correcto(usuario_cajero):
    dependency = RequireRole(RolUsuario.CAJERO)
    resultado = await dependency(usuario_cajero)
    assert resultado == usuario_cajero


@pytest.mark.asyncio
async def test_require_role_usuario_sin_rol_correcto(usuario_vendedor):
    dependency = RequireRole(RolUsuario.CAJERO)
    with pytest.raises(UsuarioNoAutorizadoError) as exc_info:
        await dependency(usuario_vendedor)
    assert "CAJERO" in str(exc_info.value)


# ── RequireAnyRole ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_require_any_role_usuario_tiene_primer_rol(usuario_vendedor):
    dependency = RequireAnyRole(RolUsuario.VENDEDOR, RolUsuario.CAJERO)
    resultado = await dependency(usuario_vendedor)
    assert resultado == usuario_vendedor


@pytest.mark.asyncio
async def test_require_any_role_usuario_tiene_segundo_rol(usuario_cajero):
    dependency = RequireAnyRole(RolUsuario.VENDEDOR, RolUsuario.CAJERO)
    resultado = await dependency(usuario_cajero)
    assert resultado == usuario_cajero


@pytest.mark.asyncio
async def test_require_any_role_usuario_no_tiene_ningun_rol(usuario_gerente):
    dependency = RequireAnyRole(RolUsuario.VENDEDOR, RolUsuario.CAJERO)
    with pytest.raises(UsuarioNoAutorizadoError) as exc_info:
        await dependency(usuario_gerente)
    assert "VENDEDOR" in str(exc_info.value)
    assert "CAJERO" in str(exc_info.value)


@pytest.mark.asyncio
async def test_require_any_role_un_solo_rol_permitido(usuario_cajero):
    dependency = RequireAnyRole(RolUsuario.CAJERO)
    resultado = await dependency(usuario_cajero)
    assert resultado == usuario_cajero


@pytest.mark.asyncio
async def test_require_any_role_un_solo_rol_no_coincide(usuario_vendedor):
    dependency = RequireAnyRole(RolUsuario.CAJERO)
    with pytest.raises(UsuarioNoAutorizadoError):
        await dependency(usuario_vendedor)
