import pytest
from app.application.use_cases.buscar_productos_use_case import BuscarProductosUseCase
from app.domain.exceptions import BusquedaInvalidaError
from app.domain.models.producto import Producto
from tests.unit.fakes.fake_producto_repository import FakeProductoRepository


@pytest.fixture
def producto_repo():
    return FakeProductoRepository()


@pytest.fixture
def use_case(producto_repo):
    return BuscarProductosUseCase(producto_repository=producto_repo)


@pytest.fixture
def camiseta_activa():
    return Producto(
        id="P-001",
        codigo="CAM-AZU-001",
        nombre="Camiseta Azul Talla M",
        categoria="Camisas",
        precio=100,
        stock_actual=15,
        estado="ACTIVO",
    )


@pytest.fixture
def pantalon_activo():
    return Producto(
        id="P-002",
        codigo="PAN-NEG-001",
        nombre="Pantalón Negro Talla M",
        categoria="Pantalones",
        precio=200,
        stock_actual=3,
        estado="ACTIVO",
    )


@pytest.fixture
def zapato_inactivo():
    return Producto(
        id="P-003",
        codigo="ZAP-CUERO-001",
        nombre="Zapatos de Cuero",
        categoria="Calzado",
        precio=150,
        stock_actual=2,
        estado="INACTIVO",
    )


# ✅ Escenario 1: Búsqueda por nombre devuelve el producto con su stock (Criterio HU-06)
@pytest.mark.asyncio
async def test_buscar_por_nombre_devuelve_producto_con_stock(
    use_case, producto_repo, camiseta_activa
):
    # Arrange
    producto_repo.agregar_producto(camiseta_activa)

    # Act
    resultados = await use_case.execute("azul")

    # Assert
    assert len(resultados) == 1
    assert resultados[0].id == "P-001"
    assert resultados[0].nombre == "Camiseta Azul Talla M"
    assert resultados[0].stock_actual == 15


# ✅ Escenario 2: Búsqueda por código escaneado con lectora (Flujo principal HU-06)
@pytest.mark.asyncio
async def test_buscar_por_codigo_escaneado(use_case, producto_repo, camiseta_activa):
    # Arrange
    producto_repo.agregar_producto(camiseta_activa)

    # Act
    resultados = await use_case.execute("CAM-AZU-001")

    # Assert
    assert len(resultados) == 1
    assert resultados[0].codigo == "CAM-AZU-001"


# ❌ Escenario 3: Término de búsqueda inválido (menos de 3 caracteres) (Caso Borde)
@pytest.mark.asyncio
async def test_rechazar_query_con_menos_de_tres_caracteres(use_case):
    # Act & Assert
    for termino in ["", "a", "ab"]:
        with pytest.raises(BusquedaInvalidaError):
            await use_case.execute(termino)


# ⚠️ Escenario 4: Sin coincidencias devuelve lista vacía sin lanzar error
# (Contrato API HU-06: responde 200 con mensaje, no es un error de dominio)
@pytest.mark.asyncio
async def test_sin_coincidencias_devuelve_lista_vacia(
    use_case, producto_repo, camiseta_activa
):
    # Arrange
    producto_repo.agregar_producto(camiseta_activa)

    # Act
    resultados = await use_case.execute("bufanda")

    # Assert
    assert resultados == []


# ❌ Escenario 5: Solo se devuelven productos en estado ACTIVO (Regla HU-06)
@pytest.mark.asyncio
async def test_no_incluir_productos_inactivos(use_case, producto_repo, zapato_inactivo):
    # Arrange
    producto_repo.agregar_producto(zapato_inactivo)

    # Act
    resultados = await use_case.execute("cuero")

    # Assert
    assert resultados == []


# 🔄 Escenario 6: El stock informado refleja siempre el valor actual (Criterio HU-06)
@pytest.mark.asyncio
async def test_stock_actualizado_se_refleja_entre_consultas(
    use_case, producto_repo, camiseta_activa
):
    # Arrange
    producto_repo.agregar_producto(camiseta_activa)

    # Act & Assert: primera consulta ve el stock inicial
    resultados = await use_case.execute("camiseta")
    assert resultados[0].stock_actual == 15

    # Simula una venta que descuenta stock entre consultas
    camiseta_activa.stock_actual = 12

    # Segunda consulta refleja el stock actualizado en tiempo real
    resultados = await use_case.execute("camiseta")
    assert resultados[0].stock_actual == 12
