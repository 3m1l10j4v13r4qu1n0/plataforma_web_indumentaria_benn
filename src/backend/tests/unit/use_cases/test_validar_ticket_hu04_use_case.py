from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from app.application.dtos.cambio_dto import ConsultarVentaPorTicketQuery
from app.application.use_cases.marcar_venta_en_cambio_use_case import (
    MarcarVentaEnCambioCommand,
    MarcarVentaEnCambioUseCase,
)
from app.application.use_cases.validar_ticket_compra_use_case import (
    ValidarTicketCompraUseCase,
)
from app.domain.exceptions import (
    DomainException,
    TicketNoEncontradoError,
    VentaYaEnCambioError,
)
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.producto import Producto
from app.domain.models.venta import EstadoVenta, Venta
from tests.unit.fakes.fake_producto_repository import FakeProductoRepository
from tests.unit.fakes.fake_venta_repository import FakeVentaRepository

TICKET_VALIDO = "T-20260601-001"
MENSAJE_ERROR_ESPERADO = (
    "El número de ticket ingresado no existe en el sistema. "
    "Verifique el comprobante."
)


@pytest.fixture
def producto_repo():
    return FakeProductoRepository()


@pytest.fixture
def venta_repo():
    return FakeVentaRepository()


@pytest.fixture
def camiseta():
    return Producto(
        id="123",
        codigo="CAM-001",
        nombre="Camiseta Azul",
        categoria="Camisetas",
        precio=25,
        stock_actual=10,
        estado="ACTIVO",
    )


@pytest.fixture
def venta_confirmada(camiseta):
    """Venta confirmada hace 5 días, tal como la describe la spec HU-04."""
    return Venta(
        id="V-001",
        fecha_hora=datetime.now() - timedelta(days=5),
        vendedor_id="C-003",
        estado=EstadoVenta.CONFIRMADA,
        numero_ticket=TICKET_VALIDO,
        total=Decimal("25.00"),
        items=[
            DetalleVenta(
                producto_id="123",
                cantidad=1,
                precio_unitario=Decimal("25.00"),
            )
        ],
    )


@pytest.fixture
def validar_ticket_use_case(venta_repo, producto_repo):
    return ValidarTicketCompraUseCase(
        venta_repository=venta_repo,
        producto_repository=producto_repo,
    )


@pytest.fixture
def marcar_en_cambio_use_case(venta_repo):
    return MarcarVentaEnCambioUseCase(venta_repository=venta_repo)


# ✅ Escenario 1 (HU-04): Ticket válido encontrado retorna los datos de la compra
@pytest.mark.asyncio
async def test_buscar_ticket_existente_retorna_datos_venta(
    validar_ticket_use_case, venta_repo, producto_repo, venta_confirmada, camiseta
):
    # Arrange
    producto_repo.agregar_producto(camiseta)
    await venta_repo.crear_venta(venta_confirmada)
    query = ConsultarVentaPorTicketQuery(numero_ticket=TICKET_VALIDO)

    # Act
    resultado = await validar_ticket_use_case.execute(query)

    # Assert: habilita continuar con el flujo de cambio
    assert resultado["existe"] is True
    assert resultado["venta_original_id"] == venta_confirmada.id
    assert resultado["numero_ticket"] == TICKET_VALIDO
    assert resultado["fecha_compra"] == venta_confirmada.fecha_hora
    assert resultado["cajero_original_id"] == "C-003"
    assert resultado["items"] == [
        {
            "producto_id": "123",
            "nombre": "Camiseta Azul",
            "cantidad": 1,
            "precio": Decimal("25.00"),
        }
    ]
    assert (
        resultado["mensaje"]
        == "Ticket válido. Puede continuar con el proceso de cambio."
    )


# ❌ Escenario 2 (HU-04): Ticket inexistente se rechaza con 404
@pytest.mark.asyncio
async def test_buscar_ticket_inexistente_retorna_404(validar_ticket_use_case):
    # Arrange
    query = ConsultarVentaPorTicketQuery(numero_ticket="T-99999999-999")

    # Act & Assert
    with pytest.raises(TicketNoEncontradoError) as exc_info:
        await validar_ticket_use_case.execute(query)

    assert exc_info.value.numero_ticket == "T-99999999-999"


# ❌ Escenario 2b (HU-04): El mensaje de error coincide exactamente con la spec
@pytest.mark.asyncio
async def test_verificar_mensaje_error_ticket_no_encontrado(
    validar_ticket_use_case,
):
    # Arrange
    query = ConsultarVentaPorTicketQuery(numero_ticket="T-00000000-000")

    # Act & Assert
    with pytest.raises(TicketNoEncontradoError) as exc_info:
        await validar_ticket_use_case.execute(query)

    assert str(exc_info.value) == MENSAJE_ERROR_ESPERADO


# ✅ Escenario 1b (HU-04): Los items muestran el precio histórico de la compra,
# aunque el precio vigente del catálogo haya cambiado
@pytest.mark.asyncio
async def test_items_muestran_precio_historico_de_la_compra(
    validar_ticket_use_case, venta_repo, producto_repo, venta_confirmada, camiseta
):
    # Arrange: el catálogo subió el precio a $30 después de la venta
    producto_repo.agregar_producto(camiseta)
    camiseta.precio = 30
    await venta_repo.crear_venta(venta_confirmada)
    query = ConsultarVentaPorTicketQuery(numero_ticket=TICKET_VALIDO)

    # Act
    resultado = await validar_ticket_use_case.execute(query)

    # Assert
    assert resultado["items"][0]["precio"] == Decimal("25.00")


# ❌ Escenario 3 (HU-04): Sin un ticket válido el flujo de cambio queda bloqueado
@pytest.mark.asyncio
async def test_bloquear_flujo_cambio_sin_ticket_valido(
    marcar_en_cambio_use_case, venta_repo
):
    # Arrange: el cliente no presenta comprobante y se intenta retener un ticket inexistente
    command = MarcarVentaEnCambioCommand(numero_ticket="T-INEXISTENTE")

    # Act & Assert: no se puede avanzar en el flujo
    with pytest.raises(TicketNoEncontradoError):
        await marcar_en_cambio_use_case.execute(command)

    # Y ninguna venta del sistema fue marcada como EN_CAMBIO
    assert all(
        venta.estado != EstadoVenta.EN_CAMBIO for venta in venta_repo.obtener_ventas()
    )


# ✅ HU-04 Endpoint opcional: retener ticket exitosamente evita doble procesamiento
@pytest.mark.asyncio
async def test_marcar_venta_en_cambio_exitoso(
    marcar_en_cambio_use_case, venta_repo, venta_confirmada
):
    # Arrange
    await venta_repo.crear_venta(venta_confirmada)
    command = MarcarVentaEnCambioCommand(numero_ticket=TICKET_VALIDO)

    # Act
    venta = await marcar_en_cambio_use_case.execute(command)

    # Assert
    assert venta.estado is EstadoVenta.EN_CAMBIO
    assert venta.numero_ticket == TICKET_VALIDO
    assert (
        await venta_repo.obtener_venta_por_numero_ticket(TICKET_VALIDO)
    ).estado is EstadoVenta.EN_CAMBIO


# ❌ HU-04 Endpoint opcional: dos cajeros compiten por el mismo ticket → conflicto
@pytest.mark.asyncio
async def test_marcar_ticket_ya_en_cambio_lanza_conflicto(
    marcar_en_cambio_use_case, venta_repo, venta_confirmada
):
    # Arrange: la caja A ya retuvo el ticket
    await venta_repo.crear_venta(venta_confirmada)
    await marcar_en_cambio_use_case.execute(
        MarcarVentaEnCambioCommand(numero_ticket=TICKET_VALIDO)
    )

    # Act & Assert: la caja B recibe conflicto
    with pytest.raises(VentaYaEnCambioError) as exc_info:
        await marcar_en_cambio_use_case.execute(
            MarcarVentaEnCambioCommand(numero_ticket=TICKET_VALIDO)
        )

    assert exc_info.value.numero_ticket == TICKET_VALIDO


# ❌ HU-04 Endpoint opcional: una venta cancelada no puede entrar en cambio
@pytest.mark.asyncio
async def test_marcar_venta_cancelada_lanza_error(
    marcar_en_cambio_use_case, venta_repo, venta_confirmada
):
    # Arrange
    venta_confirmada.estado = EstadoVenta.CANCELADA
    await venta_repo.crear_venta(venta_confirmada)

    # Act & Assert
    with pytest.raises(DomainException):
        await marcar_en_cambio_use_case.execute(
            MarcarVentaEnCambioCommand(numero_ticket=TICKET_VALIDO)
        )
