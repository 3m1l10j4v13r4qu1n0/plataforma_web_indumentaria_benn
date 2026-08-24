import pytest

from app.application.use_cases.consultar_stock_producto_use_case import (
    ConsultarStockProductoUseCase,
)
from app.domain.exceptions import ProductoNoEncontradoError
from app.domain.models.producto import Producto
from tests.unit.fakes.fake_producto_repository import FakeProductoRepository


@pytest.fixture
def producto_repo():
    return FakeProductoRepository()


@pytest.fixture
def use_case(producto_repo):
    return ConsultarStockProductoUseCase(producto_repository=producto_repo)


@pytest.fixture
def camiseta():
    return Producto(
        id="P-001",
        codigo="CAM-001",
        nombre="Camiseta Básica",
        categoria="Camisas",
        precio=100,
        stock_actual=10,
        estado="ACTIVO",
    )


# ✅ Caso Positivo: se consulta el stock de un producto existente
@pytest.mark.asyncio
async def test_consulta_stock_de_producto_existente(use_case, producto_repo, camiseta):
    # Arrange
    producto_repo.agregar_producto(camiseta)

    # Act
    producto = await use_case.execute("CAM-001")

    # Assert
    assert producto.id == "P-001"
    assert producto.codigo == "CAM-001"
    assert producto.nombre == "Camiseta Básica"
    assert producto.stock_actual == 10


# ✅ Caso Positivo: la consulta no altera el stock (operación de solo lectura)
@pytest.mark.asyncio
async def test_consulta_no_modifica_el_stock(use_case, producto_repo, camiseta):
    producto_repo.agregar_producto(camiseta)

    await use_case.execute("CAM-001")
    producto = await use_case.execute("CAM-001")

    assert producto.stock_actual == 10


# ❌ Caso Negativo: código inexistente lanza excepción de dominio (404 en handlers)
@pytest.mark.asyncio
async def test_rechaza_codigo_inexistente(use_case):
    with pytest.raises(ProductoNoEncontradoError) as exc_info:
        await use_case.execute("XXX-999")

    assert exc_info.value.identificador == "XXX-999"
