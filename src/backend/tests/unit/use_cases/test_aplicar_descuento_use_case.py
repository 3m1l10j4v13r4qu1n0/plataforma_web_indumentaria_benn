import pytest
from decimal import Decimal
from datetime import datetime, UTC

from app.application.dtos.descuento_dto import AplicarDescuentoCommand
from app.application.use_cases.aplicar_descuento_use_case import AplicarDescuentoUseCase
from app.domain.exceptions import (
    DescuentoInvalidoError,
    DescuentoSinAutorizacionError,
    DomainException,
)
from app.domain.models.venta import EstadoVenta, Venta
from app.domain.models.detalle_venta import DetalleVenta
from tests.unit.fakes.fake_descuento_repository import FakeDescuentoRepository
from tests.unit.fakes.fake_venta_repository import FakeVentaRepository
from tests.unit.fakes.fake_producto_repository import FakeProductoRepository


@pytest.fixture
def descuento_repo():
    return FakeDescuentoRepository()


@pytest.fixture
def venta_repo():
    return FakeVentaRepository()


@pytest.fixture
def producto_repo():
    return FakeProductoRepository()


@pytest.fixture
def use_case(descuento_repo, venta_repo, producto_repo):
    return AplicarDescuentoUseCase(
        descuento_repository=descuento_repo,
        venta_repository=venta_repo,
        producto_repository=producto_repo,
    )


@pytest.fixture
def venta_confirmada():
    return Venta(
        id="V-001",
        fecha_hora=datetime.now(UTC).replace(tzinfo=None),
        vendedor_id="VEN-001",
        estado=EstadoVenta.CONFIRMADA,
        numero_ticket="T-20260823-001",
        total=Decimal("1000.00"),
        items=[
            DetalleVenta(
                producto_id="P-001",
                cantidad=2,
                precio_unitario=Decimal("500.00"),
            )
        ],
    )


@pytest.fixture
def venta_pendiente():
    return Venta(
        id="V-002",
        fecha_hora=datetime.now(UTC).replace(tzinfo=None),
        vendedor_id="VEN-001",
        estado=EstadoVenta.PENDIENTE,
        total=Decimal("500.00"),
        items=[
            DetalleVenta(
                producto_id="P-001",
                cantidad=1,
                precio_unitario=Decimal("500.00"),
            )
        ],
    )


# ✅ Escenario 1: Descuento válido dentro del límite (sin autorización)
@pytest.mark.asyncio
async def test_aplicar_descuento_dentro_del_limite(
    use_case, venta_repo, venta_confirmada
):
    # Arrange
    await venta_repo.crear_venta(venta_confirmada)
    command = AplicarDescuentoCommand(
        venta_id="V-001",
        porcentaje=Decimal("10.0"),
        motivo="Promoción de temporada",
    )

    # Act
    descuento = await use_case.execute(command)

    # Assert
    assert descuento is not None
    assert descuento.porcentaje == Decimal("10.0")
    assert descuento.monto_descuento == Decimal("100.00")  # 10% de 1000
    assert descuento.autorizado_por is None
    assert descuento.motivo == "Promoción de temporada"


# ✅ Escenario 2: Descuento con autorización (supera el límite)
@pytest.mark.asyncio
async def test_aplicar_descuento_con_autorizacion(
    use_case, venta_repo, venta_confirmada
):
    # Arrange
    await venta_repo.crear_venta(venta_confirmada)
    command = AplicarDescuentoCommand(
        venta_id="V-001",
        porcentaje=Decimal("40.0"),
        motivo="Promoción especial de gerente",
        autorizado_por="GER-001",
    )

    # Act
    descuento = await use_case.execute(command)

    # Assert
    assert descuento is not None
    assert descuento.porcentaje == Decimal("40.0")
    assert descuento.monto_descuento == Decimal("400.00")  # 40% de 1000
    assert descuento.autorizado_por == "GER-001"


# ❌ Escenario 3: Descuento sin autorización que la requiere
@pytest.mark.asyncio
async def test_rechazar_descuento_sin_autorizacion(
    use_case, venta_repo, venta_confirmada
):
    # Arrange
    await venta_repo.crear_venta(venta_confirmada)
    command = AplicarDescuentoCommand(
        venta_id="V-001",
        porcentaje=Decimal("40.0"),
        motivo="Promoción especial",
        autorizado_por=None,
    )

    # Act & Assert
    with pytest.raises(DescuentoSinAutorizacionError) as exc_info:
        await use_case.execute(command)

    assert exc_info.value.porcentaje == 40.0


# ❌ Escenario 4: Venta no encontrada
@pytest.mark.asyncio
async def test_rechazar_descuento_venta_no_encontrada(use_case):
    # Arrange
    command = AplicarDescuentoCommand(
        venta_id="V-999",
        porcentaje=Decimal("10.0"),
        motivo="Descuento",
    )

    # Act & Assert
    with pytest.raises(DomainException) as exc_info:
        await use_case.execute(command)

    assert "V-999" in str(exc_info.value)


# ❌ Escenario 5: Venta no confirmada
@pytest.mark.asyncio
async def test_rechazar_descuento_venta_no_confirmada(
    use_case, venta_repo, venta_pendiente
):
    # Arrange
    await venta_repo.crear_venta(venta_pendiente)
    command = AplicarDescuentoCommand(
        venta_id="V-002",
        porcentaje=Decimal("10.0"),
        motivo="Descuento",
    )

    # Act & Assert
    with pytest.raises(DomainException) as exc_info:
        await use_case.execute(command)

    assert "no está confirmada" in str(exc_info.value)


# ❌ Escenario 6: Descuento duplicado para la misma venta
@pytest.mark.asyncio
async def test_rechazar_descuento_duplicado(use_case, venta_repo, venta_confirmada):
    # Arrange
    await venta_repo.crear_venta(venta_confirmada)
    command1 = AplicarDescuentoCommand(
        venta_id="V-001",
        porcentaje=Decimal("10.0"),
        motivo="Primer descuento",
    )
    await use_case.execute(command1)

    command2 = AplicarDescuentoCommand(
        venta_id="V-001",
        porcentaje=Decimal("5.0"),
        motivo="Segundo descuento",
    )

    # Act & Assert
    with pytest.raises(DomainException) as exc_info:
        await use_case.execute(command2)

    assert "Ya existe un descuento" in str(exc_info.value)


# ❌ Escenario 7: Porcentaje inválido (cero)
@pytest.mark.asyncio
async def test_rechazar_descuento_porcentaje_cero(
    use_case, venta_repo, venta_confirmada
):
    # Arrange
    await venta_repo.crear_venta(venta_confirmada)
    command = AplicarDescuentoCommand(
        venta_id="V-001",
        porcentaje=Decimal("0"),
        motivo="Descuento inválido",
    )

    # Act & Assert
    with pytest.raises(DescuentoInvalidoError):
        await use_case.execute(command)


# ❌ Escenario 8: Porcentaje inválido (mayor a 100)
@pytest.mark.asyncio
async def test_rechazar_descuento_porcentaje_mayor_100(
    use_case, venta_repo, venta_confirmada
):
    # Arrange
    await venta_repo.crear_venta(venta_confirmada)
    command = AplicarDescuentoCommand(
        venta_id="V-001",
        porcentaje=Decimal("150.0"),
        motivo="Descuento imposible",
    )

    # Act & Assert
    with pytest.raises(DescuentoInvalidoError):
        await use_case.execute(command)


# ⚠️ Escenario 9: Límite exacto (20%) - no requiere autorización
@pytest.mark.asyncio
async def test_descuento_limite_exacto_sin_autorizacion(
    use_case, venta_repo, venta_confirmada
):
    # Arrange
    await venta_repo.crear_venta(venta_confirmada)
    command = AplicarDescuentoCommand(
        venta_id="V-001",
        porcentaje=Decimal("20.0"),
        motivo="Descuento al límite",
    )

    # Act
    descuento = await use_case.execute(command)

    # Assert
    assert descuento.porcentaje == Decimal("20.0")
    assert descuento.autorizado_por is None


# ⚠️ Escenario 10: Justo arriba del límite (20.01%) - requiere autorización
@pytest.mark.asyncio
async def test_descuento_un_dia_mas_del_limite_requiere_autorizacion(
    use_case, venta_repo, venta_confirmada
):
    # Arrange
    await venta_repo.crear_venta(venta_confirmada)
    command = AplicarDescuentoCommand(
        venta_id="V-001",
        porcentaje=Decimal("20.01"),
        motivo="Descuento sobre el límite",
        autorizado_por="GER-002",
    )

    # Act
    descuento = await use_case.execute(command)

    # Assert
    assert descuento.porcentaje == Decimal("20.01")
    assert descuento.autorizado_por == "GER-002"
