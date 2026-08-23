class DomainException(Exception):
    """Excepción base para todas las excepciones de dominio."""

    pass


class ProductoNoEncontradoError(DomainException):
    """Se lanza cuando se intenta operar con un producto que no existe."""

    def __init__(self, identificador: str):
        self.identificador = identificador
        super().__init__(
            f"El producto con identificador '{identificador}' no existe en el sistema."
        )


class BusquedaInvalidaError(DomainException):
    """Se lanza cuando el término de búsqueda es inválido (vacío o menor a 3 caracteres)."""

    def __init__(self, query: str):
        self.query = query
        super().__init__(
            f"El término de búsqueda '{query}' es inválido. "
            f"Debe contener al menos 3 caracteres."
        )


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


class ProductoInvalidoError(DomainException):
    """Se lanza cuando el producto no está en estado ACTIVO."""

    def __init__(self, producto_id: str, estado: str):
        self.producto_id = producto_id
        self.estado = estado
        super().__init__(
            f"El producto con ID '{producto_id}' no está activo (Estado: {estado})."
        )


class TicketDuplicadoError(DomainException):
    """Se lanza cuando se intenta registrar una venta con un número de ticket ya existente."""

    def __init__(self, numero_ticket: str):
        self.numero_ticket = numero_ticket
        super().__init__(
            f"El número de ticket '{numero_ticket}' ya existe en el sistema."
        )


class DescuentoExcedeLimiteError(DomainException):
    """Se lanza cuando un descuento supera el porcentaje máximo sin autorización."""

    def __init__(self, porcentaje: float, limite: float = 20.0):
        self.porcentaje = porcentaje
        self.limite = limite
        super().__init__(
            f"El descuento de {porcentaje}% supera el límite permitido de {limite}%. "
            "Se requiere autorización de gerente."
        )


class DescuentoSinAutorizacionError(DomainException):
    """Se lanza cuando se intenta aplicar un descuento que requiere autorización sin registrarla."""

    def __init__(self, porcentaje: float):
        self.porcentaje = porcentaje
        super().__init__(
            f"El descuento de {porcentaje}% requiere autorización de gerente. "
            "Debe proporcionar el ID del gerente que autoriza la operación."
        )


class DescuentoInvalidoError(DomainException):
    """Se lanza cuando los datos del descuento son inválidos."""

    def __init__(self, motivo: str):
        self.motivo = motivo
        super().__init__(f"Descuento inválido: {motivo}")
