import pytest
from app.application.dtos.venta_dto import CrearVentaCommand, ItemVentaDTO
from app.application.use_cases.validar_stock_venta_use_case import (
    ValidarStockVentaUseCase,
)
from app.domain.exceptions import (
    EstadoProductoInvalidoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
)
from app.domain.models.producto import Producto
from tests.unit.fakes.fake_producto_repository import FakeProductoRepository
from tests.unit.fakes.fake_venta_repository import FakeVentaRepository


@pytest.fixture
def producto_repo():
    return FakeProductoRepository()


@pytest.fixture
def venta_repo():
    return FakeVentaRepository()


@pytest.fixture
def use_case(producto_repo, venta_repo):
    return ValidarStockVentaUseCase(
        producto_repository=producto_repo, venta_repository=venta_repo
    )


@pytest.fixture
def producto_activo_con_stock():
    return Producto(
        id="P-001",
        codigo="CAM-001",
        nombre="Camiseta Básica",
        stock_actual=5,
        estado="ACTIVO",
    )


@pytest.fixture
def producto_sin_stock():
    return Producto(
        id="P-002", codigo="PAN-001", nombre="Pantalón", stock_actual=0, estado="ACTIVO"
    )


@pytest.fixture
def producto_inactivo():
    return Producto(
        id="P-003",
        codigo="ZAP-001",
        nombre="Zapatos",
        stock_actual=2,
        estado="INACTIVO",
    )


# ✅ Escenario 1: Venta con stock disponible (Caso Positivo)
@pytest.mark.asyncio
async def test_validar_venta_con_stock_suficiente(
    use_case, producto_repo, venta_repo, producto_activo_con_stock
):
    # Arrange
    producto_repo.agregar_producto(producto_activo_con_stock)
    command = CrearVentaCommand(
        vendedor_id="V-001", items=[ItemVentaDTO(producto_id="P-001", cantidad=2)]
    )

    # Act
    venta = await use_case.execute(command)

    # Assert
    assert venta is not None
    assert venta.vendedor_id == "V-001"
    assert venta.estado == "CONFIRMADA"
    assert len(venta.items) == 1
    assert venta.items[0].cantidad == 2

    # Verificar actualización automática del stock post-venta (Requisito HU-01)
    producto_actualizado = await producto_repo.obtener_por_id("P-001")
    assert producto_actualizado.stock_actual == 3

    assert len(venta_repo.obtener_ventas()) == 1


# ❌ Escenario 2: Venta con stock en cero (Caso Negativo)
@pytest.mark.asyncio
async def test_rechazar_venta_con_stock_en_cero(
    use_case, producto_repo, producto_sin_stock
):
    # Arrange
    producto_repo.agregar_producto(producto_sin_stock)
    command = CrearVentaCommand(
        vendedor_id="V-001", items=[ItemVentaDTO(producto_id="P-002", cantidad=1)]
    )

    # Act & Assert
    with pytest.raises(StockInsuficienteError) as exc_info:
        await use_case.execute(command)

    assert exc_info.value.producto_id == "P-002"
    assert exc_info.value.stock_actual == 0
    assert exc_info.value.cantidad_solicitada == 1


# ⚠️ Escenario 3: Validación de cantidad mayor al stock (Caso Borde)
@pytest.mark.asyncio
async def test_rechazar_venta_cantidad_mayor_al_stock(
    use_case, producto_repo, producto_activo_con_stock
):
    # Arrange
    producto_repo.agregar_producto(producto_activo_con_stock)  # Stock = 5
    command = CrearVentaCommand(
        vendedor_id="V-001", items=[ItemVentaDTO(producto_id="P-001", cantidad=6)]
    )  # Solicita 6

    # Act & Assert
    with pytest.raises(StockInsuficienteError) as exc_info:
        await use_case.execute(command)

    assert exc_info.value.stock_actual == 5
    assert exc_info.value.cantidad_solicitada == 6


# ❌ Escenario 4: Producto no encontrado
@pytest.mark.asyncio
async def test_rechazar_venta_producto_no_encontrado(use_case):
    # Arrange
    command = CrearVentaCommand(
        vendedor_id="V-001", items=[ItemVentaDTO(producto_id="P-999", cantidad=1)]
    )

    # Act & Assert
    with pytest.raises(ProductoNoEncontradoError) as exc_info:
        await use_case.execute(command)

    assert exc_info.value.producto_id == "P-999"


# ❌ Escenario 5: Producto inactivo
@pytest.mark.asyncio
async def test_rechazar_venta_producto_inactivo(
    use_case, producto_repo, producto_inactivo
):
    # Arrange
    producto_repo.agregar_producto(producto_inactivo)
    command = CrearVentaCommand(
        vendedor_id="V-001", items=[ItemVentaDTO(producto_id="P-003", cantidad=1)]
    )

    # Act & Assert
    with pytest.raises(EstadoProductoInvalidoError) as exc_info:
        await use_case.execute(command)

    assert exc_info.value.producto_id == "P-003"
    assert exc_info.value.estado == "INACTIVO"
