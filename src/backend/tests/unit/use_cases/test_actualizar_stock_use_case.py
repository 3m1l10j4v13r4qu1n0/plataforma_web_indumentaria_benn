import pytest

from app.application.use_cases.actualizar_stock_use_case import ActualizarStockUseCase
from app.domain.exceptions import (
    CantidadMovimientoInvalidaError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
    StockUpdateException,
)
from app.domain.models.movimiento_stock import TipoMovimiento
from app.domain.models.producto import Producto
from tests.unit.fakes.fake_movimiento_stock_repository import (
    FakeMovimientoStockRepository,
)
from tests.unit.fakes.fake_producto_repository import FakeProductoRepository
from tests.unit.fakes.fake_unit_of_work import FakeUnitOfWork


class FakeProductoRepositoryTransaccional(FakeProductoRepository):
    """Fake con semántica transaccional: las lecturas devuelven copias y solo
    `actualizar_stock` escribe en el almacenamiento. Permite verificar que,
    si la actualización falla, el stock persistido queda en su valor original."""

    def __init__(self):
        super().__init__()
        self._fallar_actualizacion = False

    def activar_fallo_de_actualizacion(self) -> None:
        self._fallar_actualizacion = True

    def _copiar(self, producto: Producto) -> Producto:
        return Producto(
            id=producto.id,
            codigo=producto.codigo,
            nombre=producto.nombre,
            categoria=producto.categoria,
            precio=producto.precio,
            stock_actual=producto.stock_actual,
            estado=producto.estado,
        )

    async def obtener_por_id(self, producto_id: str) -> Producto | None:
        producto = self._productos.get(producto_id)
        return self._copiar(producto) if producto else None

    async def actualizar_stock(self, producto_id: str, nuevo_stock: int) -> None:
        if self._fallar_actualizacion:
            raise RuntimeError("Simulación de fallo de BD al actualizar stock")
        await super().actualizar_stock(producto_id, nuevo_stock)


@pytest.fixture
def producto_repo():
    return FakeProductoRepository()


@pytest.fixture
def movimiento_repo():
    return FakeMovimientoStockRepository()


@pytest.fixture
def uow():
    return FakeUnitOfWork()


@pytest.fixture
def use_case(producto_repo, movimiento_repo, uow):
    return ActualizarStockUseCase(
        producto_repository=producto_repo,
        movimiento_stock_repository=movimiento_repo,
        unit_of_work=uow,
    )


@pytest.fixture
def producto_con_stock_10():
    return Producto(
        id="P-001",
        codigo="CAM-001",
        nombre="Camiseta Básica",
        categoria="Camisas",
        precio=100,
        stock_actual=10,
        estado="ACTIVO",
    )


# ✅ Escenario 1 (HU-08): descuento automático de stock por venta (Caso Positivo)
@pytest.mark.asyncio
async def test_descuento_automatico_de_stock_al_vender(
    use_case, producto_repo, uow, producto_con_stock_10
):
    # Arrange
    producto_repo.agregar_producto(producto_con_stock_10)

    # Act
    nuevo_stock = await use_case.execute(
        producto_id="P-001",
        cantidad=1,
        tipo_movimiento=TipoMovimiento.VENTA,
        documento_referencia_id="V-001",
    )

    # Assert: stock 9 inmediatamente y transacción confirmada una sola vez
    assert nuevo_stock == 9
    producto_actualizado = await producto_repo.obtener_por_id("P-001")
    assert producto_actualizado.stock_actual == 9
    assert uow.commits == 1


# ✅ Escenario 2 (HU-08): incremento automático de stock por devolución (Caso Positivo)
@pytest.mark.asyncio
async def test_incremento_automatico_de_stock_al_devolver(use_case, producto_repo):
    # Arrange
    producto = Producto(
        id="P-002",
        codigo="PAN-001",
        nombre="Pantalón",
        categoria="Pantalones",
        precio=200,
        stock_actual=5,
        estado="ACTIVO",
    )
    producto_repo.agregar_producto(producto)

    # Act
    nuevo_stock = await use_case.execute(
        producto_id="P-002",
        cantidad=2,
        tipo_movimiento=TipoMovimiento.DEVOLUCION,
        documento_referencia_id="C-001",
    )

    # Assert: stock 7 inmediatamente
    assert nuevo_stock == 7
    producto_actualizado = await producto_repo.obtener_por_id("P-002")
    assert producto_actualizado.stock_actual == 7


# ✅ Escenario 3 (HU-08): creación de registros en movimientos_stock (auditoría)
@pytest.mark.asyncio
async def test_verificar_creacion_de_registro_en_movimientos_stock(
    use_case, producto_repo, movimiento_repo, producto_con_stock_10
):
    # Arrange
    producto_repo.agregar_producto(producto_con_stock_10)

    # Act: venta de 1 unidad y luego devolución de 2 unidades
    await use_case.execute(
        producto_id="P-001",
        cantidad=1,
        tipo_movimiento=TipoMovimiento.VENTA,
        documento_referencia_id="V-123",
    )
    await use_case.execute(
        producto_id="P-001",
        cantidad=2,
        tipo_movimiento=TipoMovimiento.DEVOLUCION,
        documento_referencia_id="C-456",
    )

    # Assert: ambos movimientos quedaron auditados con signo correcto
    movimientos = movimiento_repo.obtener_por_producto("P-001")
    assert len(movimientos) == 2

    venta = movimientos[0]
    assert venta.tipo_movimiento == TipoMovimiento.VENTA
    assert venta.cantidad == -1
    assert venta.documento_referencia_id == "V-123"
    assert venta.fecha_hora is not None

    devolucion = movimientos[1]
    assert devolucion.tipo_movimiento == TipoMovimiento.DEVOLUCION
    assert devolucion.cantidad == 2
    assert devolucion.documento_referencia_id == "C-456"


# ✅ Escenario 4 (HU-08): rollback si falla la actualización de stock
@pytest.mark.asyncio
async def test_rollback_de_transaccion_si_falla_la_actualizacion_de_stock(
    producto_con_stock_10, movimiento_repo, uow
):
    # Arrange: repositorio que falla al intentar escribir el stock
    producto_repo = FakeProductoRepositoryTransaccional()
    producto_repo.agregar_producto(producto_con_stock_10)
    producto_repo.activar_fallo_de_actualizacion()

    use_case = ActualizarStockUseCase(
        producto_repository=producto_repo,
        movimiento_stock_repository=movimiento_repo,
        unit_of_work=uow,
    )

    # Act & Assert: se lanza StockUpdateException
    with pytest.raises(StockUpdateException) as exc_info:
        await use_case.execute(
            producto_id="P-001",
            cantidad=1,
            tipo_movimiento=TipoMovimiento.VENTA,
            documento_referencia_id="V-999",
        )

    assert exc_info.value.producto_id == "P-001"

    # La transacción se revirtió y nunca se confirmó
    assert uow.rollbacks == 1
    assert uow.commits == 0

    # El stock persistido conserva su valor original (consistencia ACID)
    producto_persistido = await producto_repo.obtener_por_id("P-001")
    assert producto_persistido.stock_actual == 10

    # No quedó registrado ningún movimiento huérfano
    assert movimiento_repo.obtener_todos() == []


# ⚠️ Borde: venta que deja el stock exactamente en cero es permitida
@pytest.mark.asyncio
async def test_venta_que_deja_stock_en_cero_es_permitida(use_case, producto_repo, uow):
    producto = Producto(
        id="P-003",
        codigo="ZAP-001",
        nombre="Zapatos",
        categoria="Calzado",
        precio=150,
        stock_actual=1,
        estado="ACTIVO",
    )
    producto_repo.agregar_producto(producto)

    nuevo_stock = await use_case.execute(
        producto_id="P-003", cantidad=1, tipo_movimiento=TipoMovimiento.VENTA
    )

    assert nuevo_stock == 0
    assert uow.commits == 1


# ❌ Negativo: venta que dejaría el stock negativo es rechazada con rollback
@pytest.mark.asyncio
async def test_rechaza_venta_que_dejaria_stock_negativo(
    use_case, producto_repo, movimiento_repo, uow, producto_con_stock_10
):
    producto_repo.agregar_producto(producto_con_stock_10)

    with pytest.raises(StockInsuficienteError):
        await use_case.execute(
            producto_id="P-001", cantidad=11, tipo_movimiento=TipoMovimiento.VENTA
        )

    assert uow.rollbacks == 1
    assert uow.commits == 0
    assert movimiento_repo.obtener_todos() == []


# ❌ Negativo: producto inexistente
@pytest.mark.asyncio
async def test_rechaza_producto_inexistente(use_case, movimiento_repo, uow):
    with pytest.raises(ProductoNoEncontradoError) as exc_info:
        await use_case.execute(
            producto_id="P-999", cantidad=1, tipo_movimiento=TipoMovimiento.VENTA
        )

    assert exc_info.value.identificador == "P-999"
    assert uow.rollbacks == 1
    assert movimiento_repo.obtener_todos() == []


# ❌ Borde: cantidad cero o negativa es inválida
@pytest.mark.asyncio
async def test_rechaza_cantidad_invalida(use_case, uow, producto_con_stock_10):
    for cantidad in [0, -3]:
        with pytest.raises(CantidadMovimientoInvalidaError):
            await use_case.execute(
                producto_id="P-001",
                cantidad=cantidad,
                tipo_movimiento=TipoMovimiento.VENTA,
            )

    assert uow.rollbacks == 2
