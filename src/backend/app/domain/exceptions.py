# HU-01 exceptions


class DomainException(Exception):
    """Excepción base para todas las excepciones de dominio."""

    pass


class ProductoNoEncontradoError(DomainException):
    """Se lanza cuando se intenta operar con un producto que no existe."""

    def __init__(self, codigo: str):
        self.codigo = codigo
        super().__init__(f"El producto con código '{codigo}' no existe en el sistema.")


class StockInsuficienteError(DomainException):
    """Se lanza cuando el stock actual es menor a la cantidad solicitada o es cero."""

    def __init__(
        self,
        producto_id: str,
        nombre_producto: str,
        stock_actual: int,
        cantidad_solicitada: int,
    ):
        self.producto_id = producto_id
        self.nombre_producto = nombre_producto
        self.stock_actual = stock_actual
        self.cantidad_solicitada = cantidad_solicitada
        super().__init__(
            f"Stock insuficiente para '{nombre_producto}'. "
            f"Disponible: {stock_actual}, Solicitado: {cantidad_solicitada}."
        )


class EstadoProductoInvalidoError(DomainException):
    """Se lanza cuando el producto no está en estado ACTIVO."""

    def __init__(self, producto_id: str, estado: str):
        self.producto_id = producto_id
        self.estado = estado
        super().__init__(
            f"El producto con ID '{producto_id}' no está activo (Estado: {estado})."
        )


# HU-05 exceptions


class DescuentoExcedeLimiteError(DomainException):
    """Se lanza cuando el descuento supera el límite permitido sin autorización."""

    def __init__(self, porcentaje_solicitado: float, limite_permitido: float):
        self.porcentaje_solicitado = porcentaje_solicitado
        self.limite_permitido = limite_permitido
        super().__init__(
            f"El descuento del {porcentaje_solicitado}% excede el límite permitido del {limite_permitido}%. "
            f"Se requiere autorización de un Gerente."
        )


class UsuarioNoAutorizadoError(DomainException):
    """Se lanza cuando un usuario intenta autorizar una operación sin tener el rol requerido."""

    def __init__(self, usuario_id: str, rol_requerido: str):
        self.usuario_id = usuario_id
        self.rol_requerido = rol_requerido
        super().__init__(
            f"El usuario con ID '{usuario_id}' no tiene el rol '{rol_requerido}' "
            f"necesario para autorizar esta operación."
        )


# HU-02 exceptions


class PlazoDeCambioVencidoError(DomainException):
    """Se lanza cuando se intenta solicitar un cambio fuera del plazo de 15 días."""

    def __init__(self, numero_ticket: str, fecha_compra: str, dias_transcurridos: int):
        self.numero_ticket = numero_ticket
        self.fecha_compra = fecha_compra
        self.dias_transcurridos = dias_transcurridos
        super().__init__(
            f"El plazo para cambiar el producto del ticket '{numero_ticket}' ha vencido. "
            f"Fecha de compra: {fecha_compra}. Días transcurridos: {dias_transcurridos}. "
            f"El límite máximo es de 15 días calendario."
        )


class VentaNoEncontradaError(DomainException):
    """Se lanza cuando se intenta operar con una venta/ticket que no existe."""

    def __init__(self, identificador: str):
        self.identificador = identificador
        super().__init__(
            f"No se encontró ninguna venta o ticket con el identificador '{identificador}'."
        )


# HU-03 exceptions


class ProductoNoAptoParaCambioError(DomainException):
    """Se lanza cuando el producto no cumple con las condiciones para ser cambiado."""

    def __init__(self, condicion: str):
        self.condicion = condicion
        super().__init__(
            f"El producto no cumple con las condiciones para cambio. "
            f"Debe estar 'NUEVO_CON_ETIQUETA'. Estado declarado: '{condicion}'."
        )


# HU-04 exceptions


class ProductoNoPerteneceAVentaError(DomainException):
    """Se lanza cuando se intenta cambiar un producto que no está en el ticket original."""

    def __init__(self, producto_id: str, numero_ticket: str):
        self.producto_id = producto_id
        self.numero_ticket = numero_ticket
        super().__init__(
            f"El producto con ID '{producto_id}' no se encuentra en el comprobante '{numero_ticket}'."
        )


# HU-08 exceptions


class TipoMovimientoInvalidoError(DomainException):
    """Se lanza cuando se intenta registrar un movimiento con un tipo no permitido."""

    def __init__(self, tipo: str):
        self.tipo = tipo
        super().__init__(
            f"Tipo de movimiento '{tipo}' no es válido. "
            f"Debe ser 'VENTA', 'DEVOLUCION', 'CAMBIO' o 'AJUSTE'."
        )


class CantidadMovimientoInvalidaError(DomainException):
    """Se lanza cuando se intenta registrar un movimiento con cantidad cero."""

    def __init__(self, cantidad: int):
        self.cantidad = cantidad
        super().__init__(
            f"La cantidad del movimiento no puede ser cero. Valor recibido: {cantidad}."
        )
