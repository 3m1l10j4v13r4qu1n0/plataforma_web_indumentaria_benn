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


@pytest.mark.asyncio
async def test_consultar_stock_por_codigo_devuelve_productos_coincidentes(
    use_case, producto_repo
):
    producto_repo.agregar_producto(
        Producto(
            id="P-001",
            codigo="CAM-001",
            nombre="Camiseta Básica",
            categoria_id=1,
            precio=1000,
            stock_actual=5,
            estado="ACTIVO",
        )
    )

    productos = await use_case.execute("cam")

    assert len(productos) == 1
    assert productos[0].codigo == "CAM-001"
    assert productos[0].stock_actual == 5


@pytest.mark.asyncio
async def test_consultar_stock_sin_resultados_lanza_error_de_dominio(use_case):
    with pytest.raises(ProductoNoEncontradoError):
        await use_case.execute("inexistente")
