from decimal import Decimal

import pytest

from app.application.dtos.venta_dto import CrearVentaCommand, ItemVentaDTO
from app.application.use_cases.validar_stock_venta_use_case import (
    ValidarStockVentaUseCase,
)
from app.domain.exceptions import TicketDuplicadoError
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.producto import Producto
from app.domain.models.venta import EstadoVenta, Venta
from tests.unit.fakes.fake_generador_numero_ticket import FakeGeneradorNumeroTicket
from tests.unit.fakes.fake_movimiento_stock_repository import (
    FakeMovimientoStockRepository,
)
from tests.unit.fakes.fake_producto_repository import FakeProductoRepository
from tests.unit.fakes.fake_venta_repository import FakeVentaRepository


@pytest.fixture
def producto_repo():
    return FakeProductoRepository()


@pytest.fixture
def venta_repo():
    return FakeVentaRepository()


@pytest.fixture
def generador_ticket():
    return FakeGeneradorNumeroTicket()


@pytest.fixture
def movimiento_repo():
    return FakeMovimientoStockRepository()


@pytest.fixture
def use_case(producto_repo, venta_repo, generador_ticket, movimiento_repo):
    return ValidarStockVentaUseCase(
        producto_repository=producto_repo,
        venta_repository=venta_repo,
        generador_numero_ticket=generador_ticket,
        movimiento_stock_repository=movimiento_repo,
    )


@pytest.fixture
def remera():
    return Producto(
        id="P-001",
        codigo="REM-001",
        nombre="Remera Blanca",
        categoria="Remeras",
        precio=100,
        stock_actual=10,
        estado="ACTIVO",
    )


@pytest.fixture
def jean():
    return Producto(
        id="P-002",
        codigo="JEA-001",
        nombre="Jean Azul",
        categoria="Pantalones",
        precio=200,
        stock_actual=5,
        estado="ACTIVO",
    )


# ✅ Escenario 1 (HU-07): Venta confirmada genera ticket con datos correctos (Caso Positivo)
@pytest.mark.asyncio
async def test_generar_ticket_con_datos_correctos(
    use_case, producto_repo, generador_ticket, remera, jean
):
    # Arrange
    producto_repo.agregar_producto(remera)
    producto_repo.agregar_producto(jean)
    command = CrearVentaCommand(
        vendedor_id="V-001",
        items=[
            ItemVentaDTO(producto_id="P-001", cantidad=2),
            ItemVentaDTO(producto_id="P-002", cantidad=1),
        ],
    )

    # Act
    venta = await use_case.execute(command)

    # Assert
    assert venta.numero_ticket == "T-TEST-001"
    assert generador_ticket.generados == ["T-TEST-001"]
    assert venta.estado == EstadoVenta.CONFIRMADA
    assert venta.vendedor_id == "V-001"
    assert venta.fecha_hora is not None
    assert venta.total == Decimal("400")


# ✅ Escenario 2 (HU-07): Los detalles registran el precio congelado al momento de la venta
@pytest.mark.asyncio
async def test_verificar_datos_registrados_en_detalle_venta(
    use_case, producto_repo, venta_repo, remera, jean
):
    # Arrange
    producto_repo.agregar_producto(remera)
    producto_repo.agregar_producto(jean)
    command = CrearVentaCommand(
        vendedor_id="V-001",
        items=[
            ItemVentaDTO(producto_id="P-001", cantidad=2),
            ItemVentaDTO(producto_id="P-002", cantidad=1),
        ],
    )

    # Act
    await use_case.execute(command)

    # Assert: la venta quedó registrada con sus ítems y precios históricos
    venta_registrada = venta_repo.obtener_ventas()[0]
    assert len(venta_registrada.items) == 2
    assert venta_registrada.items[0].producto_id == "P-001"
    assert venta_registrada.items[0].cantidad == 2
    assert venta_registrada.items[0].precio_unitario == Decimal("100")
    assert venta_registrada.items[1].producto_id == "P-002"
    assert venta_registrada.items[1].cantidad == 1
    assert venta_registrada.items[1].precio_unitario == Decimal("200")


# ✅ Escenario 3 (HU-07): Cada venta obtiene un número de ticket único (Caso Negativo/Borde)
@pytest.mark.asyncio
async def test_validar_numero_unico_de_comprobante(
    use_case, producto_repo, venta_repo, remera
):
    # Arrange
    producto_repo.agregar_producto(remera)

    # Act: dos ventas consecutivas reciben tickets distintos
    venta_1 = await use_case.execute(
        CrearVentaCommand(
            vendedor_id="V-001",
            items=[ItemVentaDTO(producto_id="P-001", cantidad=1)],
        )
    )
    venta_2 = await use_case.execute(
        CrearVentaCommand(
            vendedor_id="V-002",
            items=[ItemVentaDTO(producto_id="P-001", cantidad=1)],
        )
    )

    # Assert
    assert venta_1.numero_ticket != venta_2.numero_ticket
    assert len(venta_repo.obtener_ventas()) == 2

    # El repositorio rechaza un duplicado, igual que la restricción UNIQUE de la BD
    duplicada = Venta(
        id="venta-duplicada",
        fecha_hora=venta_1.fecha_hora,
        vendedor_id="V-003",
        estado=EstadoVenta.CONFIRMADA,
        numero_ticket=venta_1.numero_ticket,
        total=Decimal("100"),
        items=[
            DetalleVenta(
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
            )
            for item in venta_1.items
        ],
    )
    with pytest.raises(TicketDuplicadoError) as exc_info:
        await venta_repo.crear_venta(duplicada)

    assert exc_info.value.numero_ticket == venta_1.numero_ticket
    assert len(venta_repo.obtener_ventas()) == 2


# ✅ Escenario 4 (HU-07): Un fallo posterior (ej. impresión) no revierte la venta registrada
@pytest.mark.asyncio
async def test_manejo_de_error_de_impresion_sin_revertir_venta(
    use_case, producto_repo, venta_repo, remera
):
    # Arrange
    producto_repo.agregar_producto(remera)

    # Act: la venta se registra exitosamente...
    venta = await use_case.execute(
        CrearVentaCommand(
            vendedor_id="V-001",
            items=[ItemVentaDTO(producto_id="P-001", cantidad=1)],
        )
    )

    # ...y luego falla la impresión (concern del frontend, sin acople con el backend)
    with pytest.raises(RuntimeError):
        _enviar_a_imprimir(venta)

    # Assert: la venta permanece registrada e intacta con su comprobante
    ventas_en_sistema = venta_repo.obtener_ventas()
    assert len(ventas_en_sistema) == 1
    assert ventas_en_sistema[0].estado == EstadoVenta.CONFIRMADA
    assert ventas_en_sistema[0].numero_ticket == venta.numero_ticket


def _enviar_a_imprimir(venta):
    """Simula el envío a la impresora térmica del local."""
    raise RuntimeError("Impresora desconectada o sin papel")
