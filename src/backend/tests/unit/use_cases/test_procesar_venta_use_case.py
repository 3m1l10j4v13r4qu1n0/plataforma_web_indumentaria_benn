import uuid
from datetime import datetime

import pytest
from app.application.dtos.venta_dto import CrearVentaCommand, ItemVentaDTO
from app.application.use_cases.procesar_venta_use_case import ProcesarVentaUseCase
from app.domain.exceptions import (
    DescuentoExcedeLimiteError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
    UsuarioNoAutorizadoError,
)
from app.domain.models.producto import Producto
from tests.unit.fakes.fake_movimiento_stock_repository import (
    FakeMovimientoStockRepository,
)
from tests.unit.fakes.fake_producto_repository import FakeProductoRepository
from tests.unit.fakes.fake_unit_of_work import FakeUnitOfWork
from tests.unit.fakes.fake_usuario_repository import FakeUsuarioRepository
from tests.unit.fakes.fake_venta_repository import FakeVentaRepository


@pytest.fixture
def producto_repo():
    return FakeProductoRepository()


@pytest.fixture
def venta_repo():
    return FakeVentaRepository()


@pytest.fixture
def usuario_repo():
    return FakeUsuarioRepository()


@pytest.fixture
def unit_of_work():
    return FakeUnitOfWork()


@pytest.fixture
def use_case(
    producto_repo, venta_repo, usuario_repo, movimiento_stock_repo, unit_of_work
):
    return ProcesarVentaUseCase(
        producto_repository=producto_repo,
        venta_repository=venta_repo,
        usuario_repository=usuario_repo,
        movimiento_stock_repository=movimiento_stock_repo,
        unit_of_work=unit_of_work,
    )


@pytest.fixture
def producto_activo_con_stock():
    return Producto(
        id="P-001",
        codigo="CAM-001",
        nombre="Camiseta Básica",
        stock_actual=10,
        estado="ACTIVO",
    )


# ✅ Escenario HU-05.1: Venta con descuento dentro del límite permitido (<= 20%) sin gerente
@pytest.mark.asyncio
async def test_venta_con_descuento_valido_sin_gerente(
    use_case, producto_repo, venta_repo, producto_activo_con_stock
):
    # Arrange
    producto_repo.agregar_producto(producto_activo_con_stock)
    command = CrearVentaCommand(
        vendedor_id="V-001",
        items=[ItemVentaDTO(producto_id="P-001", cantidad=2)],
        porcentaje_descuento=15.0,  # Dentro del límite de 20%
        gerente_autorizacion_id=None,
    )

    # Act
    venta = await use_case.execute(command)

    # Assert
    assert venta.descuento.porcentaje == 15.0
    assert venta.descuento.gerente_autorizacion_id is None
    assert venta.estado == "CONFIRMADA"


# ✅ Escenario HU-05.2: Venta con descuento alto (> 20%) CON autorización válida de gerente
@pytest.mark.asyncio
async def test_venta_con_descuento_alto_y_autorizacion_gerente_valida(
    use_case, producto_repo, venta_repo, producto_activo_con_stock
):
    # Arrange
    producto_repo.agregar_producto(producto_activo_con_stock)
    command = CrearVentaCommand(
        vendedor_id="V-001",
        items=[ItemVentaDTO(producto_id="P-001", cantidad=2)],
        porcentaje_descuento=30.0,  # Supera el 20%
        gerente_autorizacion_id="GERENTE-001",  # ID válido de gerente
    )

    # Act
    venta = await use_case.execute(command)

    # Assert
    assert venta.descuento.porcentaje == 30.0
    assert venta.descuento.gerente_autorizacion_id == "GERENTE-001"
    assert venta.estado == "CONFIRMADA"


# ❌ Escenario HU-05.3: Venta con descuento alto (> 20%) SIN autorización de gerente
@pytest.mark.asyncio
async def test_rechazar_venta_descuento_alto_sin_autorizacion(
    use_case, producto_repo, producto_activo_con_stock
):
    # Arrange
    producto_repo.agregar_producto(producto_activo_con_stock)
    command = CrearVentaCommand(
        vendedor_id="V-001",
        items=[ItemVentaDTO(producto_id="P-001", cantidad=2)],
        porcentaje_descuento=25.0,  # Supera el 20%
        gerente_autorizacion_id=None,  # Sin autorización
    )

    # Act & Assert
    with pytest.raises(DescuentoExcedeLimiteError) as exc_info:
        await use_case.execute(command)

    assert exc_info.value.porcentaje_solicitado == 25.0
    assert exc_info.value.limite_permitido == 20.0


# ❌ Escenario HU-05.4: Venta con descuento alto (> 20%) CON autorización de usuario que NO es gerente
@pytest.mark.asyncio
async def test_rechazar_venta_descuento_alto_con_autorizacion_no_gerente(
    use_case, producto_repo, producto_activo_con_stock
):
    # Arrange
    producto_repo.agregar_producto(producto_activo_con_stock)
    command = CrearVentaCommand(
        vendedor_id="V-001",
        items=[ItemVentaDTO(producto_id="P-001", cantidad=2)],
        porcentaje_descuento=25.0,
        gerente_autorizacion_id="VENDEDOR-001",  # ID de un vendedor, no de un gerente
    )

    # Act & Assert
    with pytest.raises(UsuarioNoAutorizadoError) as exc_info:
        await use_case.execute(command)

    assert exc_info.value.usuario_id == "VENDEDOR-001"
    assert exc_info.value.rol_requerido == "GERENTE"


# ✅ Escenario HU-08.1: Venta exitosa con registro atómico de movimiento de stock
@pytest.mark.asyncio
async def test_procesar_venta_con_registro_atomico_de_movimiento(
    use_case,
    producto_repo,
    venta_repo,
    movimiento_stock_repo,
    unit_of_work,
    producto_activo_con_stock,
):
    # Arrange
    producto_repo.agregar_producto(producto_activo_con_stock)
    usuario_repo.agregar_usuario("V-001", "VENDEDOR")

    command = CrearVentaCommand(
        vendedor_id="V-001",
        items=[ItemVentaDTO(producto_id="P-001", cantidad=2)],
        porcentaje_descuento=0.0,
    )

    # Act
    venta = await use_case.execute(command)

    # Assert
    assert venta is not None
    assert venta.estado == "CONFIRMADA"

    # 1. Verificar que el stock se descontó
    producto_actualizado = await producto_repo.obtener_por_id("P-001")
    assert producto_actualizado.stock_actual == 3

    # 2. Verificar que se registró el movimiento de stock
    assert len(movimiento_stock_repo.movimientos) == 1
    movimiento = movimiento_stock_repo.movimientos[0]
    assert movimiento.producto_id == "P-001"
    assert movimiento.cantidad == -2  # Egreso
    assert movimiento.tipo_movimiento == "VENTA"
    assert movimiento.referencia_id == venta.id
    assert movimiento.usuario_id == "V-001"

    # 3. Verificar atomicidad: se llamó a commit y NO a rollback
    assert unit_of_work.commit_called is True
    assert unit_of_work.rollback_called is False


# ❌ Escenario HU-08.2: Fallo por stock insuficiente debe hacer rollback y NO registrar movimiento
@pytest.mark.asyncio
async def test_procesar_venta_fallida_hace_rollback_y_no_registra_movimiento(
    use_case,
    producto_repo,
    movimiento_stock_repo,
    unit_of_work,
    producto_activo_con_stock,
):
    # Arrange: Intentamos vender 10, pero solo hay 5
    producto_repo.agregar_producto(producto_activo_con_stock)

    command = CrearVentaCommand(
        vendedor_id="V-001",
        items=[ItemVentaDTO(producto_id="P-001", cantidad=10)],
        porcentaje_descuento=0.0,
    )

    # Act & Assert
    with pytest.raises(StockInsuficienteError):
        await use_case.execute(command)

    # Verificar atomicidad: NO se llamó a commit, SÍ se llamó a rollback (o al menos no commit)
    assert unit_of_work.commit_called is False
    assert unit_of_work.rollback_called is True

    # Verificar que NO se registró ningún movimiento de stock
    assert len(movimiento_stock_repo.movimientos) == 0

    # Verificar que el stock del producto NO se modificó
    producto_actualizado = await producto_repo.obtener_por_id("P-001")
    assert producto_actualizado.stock_actual == 5
