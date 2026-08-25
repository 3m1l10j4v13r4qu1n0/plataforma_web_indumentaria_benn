import pytest

from app.application.use_cases.registrar_usuario_use_case import (
    RegistrarUsuarioUseCase,
)
from app.domain.exceptions import EmailDuplicadoError
from app.domain.models.usuario import RolUsuario, Usuario
from tests.unit.fakes.fake_password_hasher import FakePasswordHasher
from tests.unit.fakes.fake_usuario_repository import FakeUsuarioRepository


@pytest.fixture
def usuario_repo():
    return FakeUsuarioRepository()


@pytest.fixture
def password_hasher():
    return FakePasswordHasher()


@pytest.fixture
def use_case(usuario_repo, password_hasher):
    return RegistrarUsuarioUseCase(
        usuario_repository=usuario_repo,
        password_hasher=password_hasher,
    )


@pytest.fixture
def usuario_previo():
    return Usuario(
        id="EXISTENTE-001",
        email="yaexiste@test.com",
        password_hash="hashed_password123",
        nombre="Usuario Ya Existente",
        rol=RolUsuario.VENDEDOR,
        activo=True,
    )


# ── Escenario 1: Registro exitoso ────────────────────────────────────
@pytest.mark.asyncio
async def test_registro_exitoso(use_case, usuario_repo):
    # Arrange
    email = "nuevo@test.com"
    password = "password123"
    nombre = "Juan Perez"
    rol = RolUsuario.CAJERO

    # Act
    resultado = await use_case.execute(email, password, nombre, rol)

    # Assert
    assert resultado is not None
    assert resultado.email == email
    assert resultado.nombre == nombre
    assert resultado.rol == RolUsuario.CAJERO
    assert resultado.activo is True
    assert resultado.password_hash == "hashed_password123"

    # Verificar que se persistió
    guardado = await usuario_repo.buscar_por_email(email)
    assert guardado is not None
    assert guardado.id == resultado.id


# ── Escenario 2: Email duplicado ─────────────────────────────────────
@pytest.mark.asyncio
async def test_email_duplicado_lanza_excepcion(
    use_case, usuario_repo, usuario_previo
):
    # Arrange
    usuario_repo.agregar_usuario(usuario_previo)

    # Act & Assert
    with pytest.raises(EmailDuplicadoError) as exc_info:
        await use_case.execute(
            email="yaexiste@test.com",
            password="password123",
            nombre="Otro Usuario",
            rol=RolUsuario.VENDEDOR,
        )
    assert exc_info.value.email == "yaexiste@test.com"


# ── Escenario 3: Password hasheado correctamente ─────────────────────
@pytest.mark.asyncio
async def test_password_hasheado_en_registro(use_case):
    # Arrange
    email = "hash@test.com"
    password = "mi_password_segura"
    nombre = "Test Hash"
    rol = RolUsuario.GERENTE

    # Act
    resultado = await use_case.execute(email, password, nombre, rol)

    # Assert
    assert resultado.password_hash == "hashed_mi_password_segura"
    assert resultado.password_hash != password


# ── Escenario 4: Rol se asigna correctamente ─────────────────────────
@pytest.mark.asyncio
async def test_rol_asignado_correctamente(use_case):
    # Arrange & Act
    usuario_vendedor = await use_case.execute(
        "vendedor@test.com", "pass123", "Vendedor Test", RolUsuario.VENDEDOR
    )
    usuario_gerente = await use_case.execute(
        "gerente@test.com", "pass123", "Gerente Test", RolUsuario.GERENTE
    )
    usuario_encargado = await use_case.execute(
        "encargado@test.com", "pass123", "Encargado Test",
        RolUsuario.ENCARGADO_VENTAS,
    )

    # Assert
    assert usuario_vendedor.rol == RolUsuario.VENDEDOR
    assert usuario_gerente.rol == RolUsuario.GERENTE
    assert usuario_encargado.rol == RolUsuario.ENCARGADO_VENTAS
