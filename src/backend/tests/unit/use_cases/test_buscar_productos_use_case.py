import pytest
from app.application.dtos.producto_dto import BuscarProductosCommand
from app.application.use_cases.buscar_productos_use_case import BuscarProductosUseCase
from app.domain.models.producto import Producto
from tests.unit.fakes.fake_producto_repository import FakeProductoRepository


@pytest.fixture
def producto_repo():
    return FakeProductoRepository()


@pytest.fixture
def use_case(producto_repo):
    return BuscarProductosUseCase(producto_repository=producto_repo)


@pytest.fixture
def productos_sample():
    return [
        Producto(
            id="P-001",
            codigo="CAM-001",
            nombre="Camiseta Básica",
            stock_actual=5,
            estado="ACTIVO",
        ),
        Producto(
            id="P-002",
            codigo="PAN-001",
            nombre="Pantalón Jeans",
            stock_actual=0,
            estado="ACTIVO",
        ),
        Producto(
            id="P-003",
            codigo="ZAP-001",
            nombre="Zapatos Deportivos",
            stock_actual=10,
            estado="INACTIVO",
        ),
    ]


# ✅ Escenario 1: Búsqueda por código exacto
@pytest.mark.asyncio
async def test_buscar_producto_por_codigo_exacto(
    use_case, producto_repo, productos_sample
):
    # Arrange
    for p in productos_sample:
        producto_repo.agregar_producto(p)

    command = BuscarProductosCommand(query="PAN-001")

    # Act
    resultado = await use_case.execute(command)

    # Assert
    assert len(resultado.productos) == 1
    assert resultado.productos[0].producto_id == "P-002"
    assert resultado.productos[0].stock_actual == 0
    assert "Se encontraron 1 producto(s)" in resultado.mensaje


# ✅ Escenario 2: Búsqueda parcial por nombre (insensible a mayúsculas/minúsculas)
@pytest.mark.asyncio
async def test_buscar_producto_por_nombre_parcial(
    use_case, producto_repo, productos_sample
):
    # Arrange
    for p in productos_sample:
        producto_repo.agregar_producto(p)

    command = BuscarProductosCommand(
        query="camis"
    )  # Debería encontrar "Camiseta Básica"

    # Act
    resultado = await use_case.execute(command)

    # Assert
    assert len(resultado.productos) == 1
    assert resultado.productos[0].nombre == "Camiseta Básica"
    assert "Se encontraron 1 producto(s)" in resultado.mensaje


# ⚠️ Escenario 3: Búsqueda sin resultados (Caso Borde/Negativo)
@pytest.mark.asyncio
async def test_buscar_producto_sin_resultados(
    use_case, producto_repo, productos_sample
):
    # Arrange
    for p in productos_sample:
        producto_repo.agregar_producto(p)

    command = BuscarProductosCommand(query="ProductoInexistenteXYZ")

    # Act
    resultado = await use_case.execute(command)

    # Assert
    assert len(resultado.productos) == 0
    assert (
        "No se encontraron productos que coincidan con 'ProductoInexistenteXYZ'"
        in resultado.mensaje
    )
