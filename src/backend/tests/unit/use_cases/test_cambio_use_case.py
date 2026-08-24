import pytest
from datetime import datetime, timedelta

from app.application.dtos.cambio_dto import ProcesarCambioCommand
from app.application.use_cases.procesar_cambio_use_case import ProcesarCambioUseCase
from app.domain.exceptions import (
    CambioPlazoVencidoError,
    VentaNoEncontradaError,
)
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.venta import EstadoVenta, Venta
from tests.unit.fakes.fake_cambio_repository import FakeCambioRepository
from tests.unit.fakes.fake_venta_repository import FakeVentaRepository


@pytest.fixture
def cambio_repo():
    return FakeCambioRepository()


@pytest.fixture
def venta_repo():
    return FakeVentaRepository()


@pytest.fixture
def procesar_cambio_use_case(cambio_repo, venta_repo):
    return ProcesarCambioUseCase(
        cambio_repository=cambio_repo,
        venta_repository=venta_repo,
        producto_repository=None,  # No necesitamos producto repository para estos tests
    )


@pytest.fixture
def venta_reciente():
    """Venta realizada hace 10 días (dentro del plazo)."""
    fecha_compra = datetime.now() - timedelta(days=10)
    return Venta(
        id="V-001",
        fecha_hora=fecha_compra,
        vendedor_id="V-001",
        estado=EstadoVenta.CONFIRMADA,
        numero_ticket="T-20231015-001",
        total=100,
        items=[
            DetalleVenta(
                producto_id="P-001",
                cantidad=1,
                precio_unitario=100,
            )
        ],
    )


@pytest.fixture
def venta_vencida():
    """Venta realizada hace 20 días (fuera del plazo)."""
    fecha_compra = datetime.now() - timedelta(days=20)
    return Venta(
        id="V-002",
        fecha_hora=fecha_compra,
        vendedor_id="V-001",
        estado=EstadoVenta.CONFIRMADA,
        numero_ticket="T-20231010-002",
        total=200,
        items=[
            DetalleVenta(
                producto_id="P-002",
                cantidad=1,
                precio_unitario=200,
            )
        ],
    )


# ✅ Escenario 1: Procesar cambio dentro del plazo
@pytest.mark.asyncio
async def test_procesar_cambio_dentro_del_plazo(
    procesar_cambio_use_case, cambio_repo, venta_repo, venta_reciente
):
    # Arrange
    await venta_repo.crear_venta(venta_reciente)
    command = ProcesarCambioCommand(
        venta_original_id="V-001",
        cajero_id="C-005",
        producto_a_cambiar_id="P-001",
        nuevo_producto_id="P-002",
        motivo="Talla incorrecta",
    )

    # Act
    cambio = await procesar_cambio_use_case.execute(command)

    # Assert
    assert cambio is not None
    assert cambio.venta_original_id == "V-001"
    assert cambio.cajero_id == "C-005"
    assert cambio.producto_a_cambiar_id == "P-001"
    assert cambio.nuevo_producto_id == "P-002"
    assert cambio.estado == "APROBADO"
    assert cambio.motivo == "Talla incorrecta"
    assert len(cambio_repo.obtener_cambios()) == 1


# ❌ Escenario 4: Procesar cambio fuera del plazo
@pytest.mark.asyncio
async def test_procesar_cambio_fuera_del_plazo(
    procesar_cambio_use_case, venta_repo, venta_vencida
):
    # Arrange
    await venta_repo.crear_venta(venta_vencida)
    command = ProcesarCambioCommand(
        venta_original_id="V-002",
        cajero_id="C-005",
        producto_a_cambiar_id="P-002",
        nuevo_producto_id="P-003",
    )

    # Act & Assert
    with pytest.raises(CambioPlazoVencidoError) as exc_info:
        await procesar_cambio_use_case.execute(command)

    assert exc_info.value.numero_ticket == "T-20231010-002"
    assert exc_info.value.dias_transcurridos == 20
    assert exc_info.value.dias_limite == 15


# ❌ Escenario 5: Procesar cambio con venta inexistente
@pytest.mark.asyncio
async def test_procesar_cambio_venta_no_encontrada(procesar_cambio_use_case):
    # Arrange
    command = ProcesarCambioCommand(
        venta_original_id="V-NO-EXISTE",
        cajero_id="C-005",
        producto_a_cambiar_id="P-001",
        nuevo_producto_id="P-002",
    )

    # Act & Assert
    with pytest.raises(VentaNoEncontradaError) as exc_info:
        await procesar_cambio_use_case.execute(command)

    assert exc_info.value.identificador == "V-NO-EXISTE"
