from datetime import datetime, timedelta

import pytest
from app.application.use_cases.consultar_ticket_use_case import ConsultarTicketUseCase
from app.domain.exceptions import VentaNoEncontradaError
from app.domain.models.descuento import Descuento
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.venta import Venta
from tests.unit.fakes.fake_venta_repository import FakeVentaRepository


@pytest.fixture
def venta_repo():
    return FakeVentaRepository()


@pytest.fixture
def use_case(venta_repo):
    return ConsultarTicketUseCase(venta_repository=venta_repo)


@pytest.fixture
def venta_confirmada():
    return Venta(
        id="V-001",
        fecha_hora=datetime.utcnow() - timedelta(days=2),
        vendedor_id="V-001",
        numero_ticket="TKT-20231025-001",
        estado="CONFIRMADA",
        items=[DetalleVenta(producto_id="P-001", cantidad=1)],
        descuento=Descuento(),
    )


@pytest.mark.asyncio
async def test_consultar_ticket_existente(use_case, venta_repo, venta_confirmada):
    # Arrange
    venta_repo.agregar_venta(venta_confirmada)

    # Act
    resultado = await use_case.execute("TKT-20231025-001")

    # Assert
    assert resultado.numero_ticket == "TKT-20231025-001"
    assert resultado.estado == "CONFIRMADA"
    assert len(resultado.items) == 1
    assert resultado.items[0].producto_id == "P-001"


@pytest.mark.asyncio
async def test_consultar_ticket_inexistente(use_case):
    # Act & Assert
    with pytest.raises(VentaNoEncontradaError) as exc_info:
        await use_case.execute("TKT-FAKE-999")

    assert exc_info.value.identificador == "TKT-FAKE-999"
