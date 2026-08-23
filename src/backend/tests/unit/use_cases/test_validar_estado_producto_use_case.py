import pytest
from datetime import datetime, timedelta

from app.application.dtos.cambio_dto import ValidarEstadoProductoCommand
from app.application.use_cases.validar_estado_producto_use_case import (
    ValidarEstadoProductoUseCase,
)
from app.domain.exceptions import (
    CambioInvalidoError,
    CambioNoEncontradoError,
    ObservacionesRequeridasError,
    ProductoNoAptoError,
)
from app.domain.models.cambio import Cambio, EstadoCambio, EstadoProducto
from tests.unit.fakes.fake_cambio_repository import FakeCambioRepository


@pytest.fixture
def cambio_repo():
    return FakeCambioRepository()


@pytest.fixture
def validar_use_case(cambio_repo):
    return ValidarEstadoProductoUseCase(cambio_repository=cambio_repo)


@pytest.fixture
def cambio_pendiente():
    """Cambio creado tras validar ticket y plazo (HU-02), pendiente de inspección física."""
    return Cambio(
        id="CB-001",
        venta_original_id="V-001",
        fecha_cambio=datetime.now(),
        cajero_id="C-005",
        producto_a_cambiar_id="P-001",
        nuevo_producto_id="P-002",
        estado=EstadoCambio.APROBADO,
        fecha_compra_original=datetime.now() - timedelta(days=10),
    )


@pytest.fixture
def command_apto():
    return ValidarEstadoProductoCommand(
        cambio_id="CB-001",
        producto_id="P-001",
        estado_producto=EstadoProducto.NUEVO_ETIQUETADO,
        tiene_etiqueta=True,
        observaciones="Producto en perfectas condiciones",
        cajero_id="C-005",
    )


# ✅ Escenario 1: Producto nuevo y etiquetado es apto
@pytest.mark.asyncio
async def test_validar_producto_nuevo_con_etiqueta_es_apto(
    validar_use_case, cambio_repo, cambio_pendiente, command_apto
):
    # Arrange
    await cambio_repo.crear_cambio(cambio_pendiente)

    # Act
    resultado = await validar_use_case.execute(command_apto)

    # Assert
    assert resultado.es_apto_para_cambio is True
    assert "continuar con el cambio" in resultado.mensaje.lower()


# ❌ Escenario 2: Producto usado debe rechazarse
@pytest.mark.asyncio
async def test_rechazar_producto_usado(validar_use_case, cambio_repo, cambio_pendiente):
    # Arrange
    await cambio_repo.crear_cambio(cambio_pendiente)
    command = ValidarEstadoProductoCommand(
        cambio_id="CB-001",
        producto_id="P-001",
        estado_producto=EstadoProducto.USADO,
        tiene_etiqueta=True,
        observaciones="Se nota uso en el cuello",
    )

    # Act & Assert
    with pytest.raises(ProductoNoAptoError) as exc_info:
        await validar_use_case.execute(command)

    assert exc_info.value.motivo == "PRODUCTO_USADO"


# ❌ Escenario 3: Producto sin etiqueta debe bloquearse
@pytest.mark.asyncio
async def test_rechazar_producto_sin_etiqueta(
    validar_use_case, cambio_repo, cambio_pendiente
):
    # Arrange
    await cambio_repo.crear_cambio(cambio_pendiente)
    command = ValidarEstadoProductoCommand(
        cambio_id="CB-001",
        producto_id="P-001",
        estado_producto=EstadoProducto.NUEVO_ETIQUETADO,
        tiene_etiqueta=False,
        observaciones="Cliente no presentó la etiqueta",
    )

    # Act & Assert
    with pytest.raises(ProductoNoAptoError) as exc_info:
        await validar_use_case.execute(command)

    assert exc_info.value.motivo == "PRODUCTO_SIN_ETIQUETA"


# ❌ Escenario 4: Producto dañado exige observaciones y se rechaza
@pytest.mark.asyncio
async def test_rechazar_producto_danado_con_observaciones_obligatorias(
    validar_use_case, cambio_repo, cambio_pendiente
):
    # Arrange
    await cambio_repo.crear_cambio(cambio_pendiente)
    command_sin_obs = ValidarEstadoProductoCommand(
        cambio_id="CB-001",
        producto_id="P-001",
        estado_producto=EstadoProducto.DANADO,
        tiene_etiqueta=True,
    )

    # Act & Assert: sin observaciones no deja registrar el rechazo
    with pytest.raises(ObservacionesRequeridasError):
        await validar_use_case.execute(command_sin_obs)

    # Act & Assert: con observaciones rechaza por producto dañado
    command_con_obs = ValidarEstadoProductoCommand(
        cambio_id="CB-001",
        producto_id="P-001",
        estado_producto=EstadoProducto.DANADO,
        tiene_etiqueta=True,
        observaciones="Botón roto",
    )
    with pytest.raises(ProductoNoAptoError) as exc_info:
        await validar_use_case.execute(command_con_obs)

    assert exc_info.value.motivo == "PRODUCTO_DANADO"


# 💾 Escenario 5: La validación aprobada queda registrada en la BD
@pytest.mark.asyncio
async def test_verificar_registro_en_bd_de_validacion_aprobada(
    validar_use_case, cambio_repo, cambio_pendiente, command_apto
):
    # Arrange
    await cambio_repo.crear_cambio(cambio_pendiente)

    # Act
    await validar_use_case.execute(command_apto)

    # Assert
    guardado = await cambio_repo.obtener_cambio_por_id("CB-001")
    assert guardado.estado == EstadoCambio.APROBADO
    assert guardado.estado_producto == EstadoProducto.NUEVO_ETIQUETADO
    assert guardado.tiene_etiqueta is True
    assert guardado.fecha_validacion is not None


# 💾 Escenario 6: El intento de cambio rechazado queda registrado en la BD (auditoría)
@pytest.mark.asyncio
async def test_verificar_registro_en_bd_de_validacion_rechazada(
    validar_use_case, cambio_repo, cambio_pendiente
):
    # Arrange
    await cambio_repo.crear_cambio(cambio_pendiente)
    command = ValidarEstadoProductoCommand(
        cambio_id="CB-001",
        producto_id="P-001",
        estado_producto=EstadoProducto.USADO,
        tiene_etiqueta=True,
        observaciones="Se nota uso en el cuello",
    )

    # Act & Assert
    with pytest.raises(ProductoNoAptoError):
        await validar_use_case.execute(command)

    guardado = await cambio_repo.obtener_cambio_por_id("CB-001")
    assert guardado.estado == EstadoCambio.RECHAZADO_ESTADO_PRODUCTO
    assert guardado.motivo == "PRODUCTO_USADO"
    assert guardado.observaciones == "Se nota uso en el cuello"
    assert guardado.fecha_validacion is not None


# ❌ Caso borde: el producto inspeccionado no corresponde al cambio
@pytest.mark.asyncio
async def test_rechazar_validacion_con_producto_distinto_al_registrado(
    validar_use_case, cambio_repo, cambio_pendiente
):
    # Arrange
    await cambio_repo.crear_cambio(cambio_pendiente)
    command = ValidarEstadoProductoCommand(
        cambio_id="CB-001",
        producto_id="P-999",
        estado_producto=EstadoProducto.NUEVO_ETIQUETADO,
        tiene_etiqueta=True,
    )

    # Act & Assert
    with pytest.raises(CambioInvalidoError):
        await validar_use_case.execute(command)


# ❌ Caso borde: el cambio sobre el que se valida no existe
@pytest.mark.asyncio
async def test_rechazar_validacion_de_cambio_inexistente(validar_use_case):
    # Arrange
    command = ValidarEstadoProductoCommand(
        cambio_id="CB-NO-EXISTE",
        producto_id="P-001",
        estado_producto=EstadoProducto.NUEVO_ETIQUETADO,
        tiene_etiqueta=True,
    )

    # Act & Assert
    with pytest.raises(CambioNoEncontradoError) as exc_info:
        await validar_use_case.execute(command)

    assert exc_info.value.cambio_id == "CB-NO-EXISTE"
