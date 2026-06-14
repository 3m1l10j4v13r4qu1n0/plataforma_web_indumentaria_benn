"""
Cubrimos los escenarios definidos en las reglas de negocio transversales y la HU-02,
verificando que se lancen las excepciones de dominio correctas.

"""

from datetime import datetime, timedelta

import pytest
from app.application.dtos.cambio_dto import ItemCambioDTO, SolicitarCambioCommand
from app.application.use_cases.solicitar_cambio_use_case import SolicitarCambioUseCase
from app.domain.exceptions import (
    PlazoDeCambioVencidoError,
    ProductoNoAptoParaCambioError,
    ProductoNoPerteneceAVentaError,
    VentaNoEncontradaError,
)
from app.domain.models.descuento import Descuento
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.producto import Producto
from app.domain.models.venta import Venta
from tests.unit.fakes.fake_producto_repository import FakeProductoRepository
from tests.unit.fakes.fake_venta_repository import FakeVentaRepository


@pytest.fixture
def venta_repo():
    return FakeVentaRepository()


@pytest.fixture
def producto_repo():
    return FakeProductoRepository()


@pytest.fixture
def use_case(venta_repo, producto_repo):
    return SolicitarCambioUseCase(
        venta_repository=venta_repo, producto_repository=producto_repo
    )


@pytest.fixture
def producto_en_catalogo():
    return Producto(
        id="P-001",
        codigo="PROD-001",
        nombre="Camiseta",
        stock_actual=5,
        estado="ACTIVO",
    )


@pytest.fixture
def venta_confirmada_reciente():
    """Venta confirmada hace 5 días (dentro del plazo de 15 días)."""
    fecha_hace_5_dias = datetime.utcnow() - timedelta(days=5)
    return Venta(
        id="V-001",
        fecha_hora=fecha_hace_5_dias,
        vendedor_id="V-001",
        numero_ticket="TKT-20231020-001",
        estado="CONFIRMADA",
        items=[DetalleVenta(producto_id="P-001", cantidad=1)],
        descuento=Descuento(),
    )


@pytest.fixture
def venta_confirmada_vencida():
    """Venta confirmada hace 20 días (fuera del plazo de 15 días)."""
    fecha_hace_20_dias = datetime.utcnow() - timedelta(days=20)
    return Venta(
        id="V-002",
        fecha_hora=fecha_hace_20_dias,
        vendedor_id="V-001",
        numero_ticket="TKT-20231005-001",
        estado="CONFIRMADA",
        items=[DetalleVenta(producto_id="P-001", cantidad=1)],
        descuento=Descuento(),
    )


@pytest.fixture
def venta_pendiente():
    """Venta en estado PENDIENTE (no elegible para cambio)."""
    return Venta(
        id="V-003",
        fecha_hora=datetime.utcnow(),
        vendedor_id="V-001",
        numero_ticket="TKT-20231025-001",
        estado="PENDIENTE",
        items=[DetalleVenta(producto_id="P-001", cantidad=1)],
        descuento=Descuento(),
    )


@pytest.fixture
def venta_con_producto_elegible():
    """Venta confirmada hace 5 días, con un item que coincide con el producto."""
    fecha = datetime.utcnow() - timedelta(days=5)
    return Venta(
        id="V-001",
        fecha_hora=fecha,
        vendedor_id="V-001",
        numero_ticket="TKT-VALID-001",
        estado="CONFIRMADA",
        items=[DetalleVenta(producto_id="P-001", cantidad=2)],  # Producto pertenece
        descuento=Descuento(),
    )


# ✅ Escenario 1: Venta elegible para cambio (dentro del plazo y CONFIRMADA)
@pytest.mark.asyncio
async def test_validar_cambio_venta_elegible(
    use_case, venta_repo, venta_confirmada_reciente
):
    # Arrange
    venta_repo.agregar_venta(venta_confirmada_reciente)
    command = SolicitarCambioCommand(
        numero_ticket="TKT-20231020-001", fecha_solicitud=datetime.utcnow()
    )

    # Act
    resultado = await use_case.execute(command)

    # Assert
    assert resultado["venta_id"] == "V-001"
    assert resultado["numero_ticket"] == "TKT-20231020-001"
    assert resultado["estado"] == "CONFIRMADA"
    assert "elegible para cambio" in resultado["mensaje"].lower()


# ❌ Escenario 2: Ticket inexistente en el sistema
@pytest.mark.asyncio
async def test_rechazar_cambio_ticket_inexistente(use_case):
    # Arrange
    command = SolicitarCambioCommand(
        numero_ticket="TKT-FAKE-999", fecha_solicitud=datetime.utcnow()
    )

    # Act & Assert
    with pytest.raises(VentaNoEncontradaError) as exc_info:
        await use_case.execute(command)

    assert exc_info.value.identificador == "TKT-FAKE-999"


# ❌ Escenario 3: Plazo de cambio vencido (> 15 días)
@pytest.mark.asyncio
async def test_rechazar_cambio_plazo_vencido(
    use_case, venta_repo, venta_confirmada_vencida
):
    # Arrange
    venta_repo.agregar_venta(venta_confirmada_vencida)
    command = SolicitarCambioCommand(
        numero_ticket="TKT-20231005-001", fecha_solicitud=datetime.utcnow()
    )

    # Act & Assert
    with pytest.raises(PlazoDeCambioVencidoError) as exc_info:
        await use_case.execute(command)

    assert exc_info.value.numero_ticket == "TKT-20231005-001"
    assert exc_info.value.dias_transcurridos >= 15  # Debería ser ~20


# ❌ Escenario 4: Venta no confirmada (ej. PENDIENTE)
@pytest.mark.asyncio
async def test_rechazar_cambio_venta_no_confirmada(
    use_case, venta_repo, venta_pendiente
):
    # Arrange
    venta_repo.agregar_venta(venta_pendiente)
    command = SolicitarCambioCommand(
        numero_ticket="TKT-20231025-001", fecha_solicitud=datetime.utcnow()
    )

    # Act & Assert
    # La entidad Venta lanzará un ValueError genérico o una excepción específica si la definimos,
    # en nuestro modelo actual lanza ValueError("Solo se pueden solicitar cambios de ventas CONFIRMADAS.")
    with pytest.raises(ValueError) as exc_info:
        await use_case.execute(command)

    assert "Solo se pueden solicitar cambios de ventas CONFIRMADAS" in str(
        exc_info.value
    )


# --- Escenarios HU-03: Validación de Condición del Producto ---


@pytest.mark.asyncio
async def test_validar_cambio_producto_con_condicion_valida(
    use_case,
    venta_repo,
    producto_repo,
    venta_con_producto_elegible,
    producto_en_catalogo,
):
    # Arrange
    venta_repo.agregar_venta(venta_con_producto_elegible)
    producto_repo.agregar_producto(producto_en_catalogo)

    command = SolicitarCambioCommand(
        numero_ticket="TKT-VALID-001",
        fecha_solicitud=datetime.utcnow(),
        items_a_cambiar=[
            ItemCambioDTO(producto_id="P-001", condicion_declarada="NUEVO_CON_ETIQUETA")
        ],
    )

    # Act
    resultado = await use_case.execute(command)

    # Assert
    assert resultado["items_validados"][0]["condicion_validada"] == "NUEVO_CON_ETIQUETA"


@pytest.mark.asyncio
async def test_rechazar_cambio_producto_usado_o_sin_etiqueta(
    use_case,
    venta_repo,
    producto_repo,
    venta_con_producto_elegible,
    producto_en_catalogo,
):
    # Arrange
    venta_repo.agregar_venta(venta_con_producto_elegible)
    producto_repo.agregar_producto(producto_en_catalogo)

    command = SolicitarCambioCommand(
        numero_ticket="TKT-VALID-001",
        fecha_solicitud=datetime.utcnow(),
        items_a_cambiar=[
            ItemCambioDTO(producto_id="P-001", condicion_declarada="USADO_SIN_ETIQUETA")
        ],
    )

    # Act & Assert
    with pytest.raises(ProductoNoAptoParaCambioError) as exc_info:
        await use_case.execute(command)

    assert "USADO_SIN_ETIQUETA" in str(exc_info.value)
    assert exc_info.value.condicion == "USADO_SIN_ETIQUETA"


# --- Escenarios HU-04: Producto no pertenece al ticket ---


@pytest.mark.asyncio
async def test_rechazar_cambio_producto_fuera_del_ticket(
    use_case,
    venta_repo,
    producto_repo,
    venta_con_producto_elegible,
    producto_en_catalogo,
):
    # Arrange: El producto P-001 está en la venta, pero intentamos cambiar P-999
    venta_repo.agregar_venta(venta_con_producto_elegible)
    producto_repo.agregar_producto(producto_en_catalogo)

    producto_externo = Producto(
        id="P-999", codigo="PROD-999", nombre="Gorra", stock_actual=10, estado="ACTIVO"
    )
    producto_repo.agregar_producto(producto_externo)

    command = SolicitarCambioCommand(
        numero_ticket="TKT-VALID-001",
        fecha_solicitud=datetime.utcnow(),
        items_a_cambiar=[
            ItemCambioDTO(producto_id="P-999", condicion_declarada="NUEVO_CON_ETIQUETA")
        ],
    )

    # Act & Assert
    with pytest.raises(ProductoNoPerteneceAVentaError) as exc_info:
        await use_case.execute(command)

    assert exc_info.value.producto_id == "P-999"
    assert exc_info.value.numero_ticket == "TKT-VALID-001"
