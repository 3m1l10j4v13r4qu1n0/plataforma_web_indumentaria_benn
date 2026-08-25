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


class StockUpdateException(DomainException):
    """Se lanza cuando falla la actualización atómica del stock y se requiere rollback."""

    def __init__(self, producto_id: str, motivo: str):
        self.producto_id = producto_id
        self.motivo = motivo
        super().__init__(
            f"Falló la actualización de stock del producto '{producto_id}': {motivo}"
        )


class CantidadMovimientoInvalidaError(DomainException):
    """Se lanza cuando la cantidad de un movimiento de stock es inválida (cero o con signo inconsistente)."""

    def __init__(self, motivo: str):
        self.motivo = motivo
        super().__init__(f"Cantidad de movimiento inválida: {motivo}")


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


class CambioNoEncontradoError(DomainException):
    """Se lanza cuando se intenta operar con un cambio que no existe."""

    def __init__(self, cambio_id: str):
        self.cambio_id = cambio_id
        super().__init__(f"El cambio con ID '{cambio_id}' no existe en el sistema.")


class CambioPlazoVencidoError(DomainException):
    """Se lanza cuando se intenta realizar un cambio fuera del plazo de 15 días."""

    def __init__(
        self, numero_ticket: str, dias_transcurridos: int, dias_limite: int = 15
    ):
        self.numero_ticket = numero_ticket
        self.dias_transcurridos = dias_transcurridos
        self.dias_limite = dias_limite
        super().__init__(
            f"El plazo de {dias_limite} días para realizar cambios ha expirado para el ticket '{numero_ticket}'. "
            f"Días transcurridos: {dias_transcurridos}."
        )


class VentaNoEncontradaError(DomainException):
    """Se lanza cuando se intenta operar con una venta que no existe."""

    def __init__(self, identificador: str):
        self.identificador = identificador
        super().__init__(
            f"La venta con identificador '{identificador}' no existe en el sistema."
        )


class TicketNoEncontradoError(DomainException):
    """Se lanza cuando el número de ticket ingresado no existe en el sistema (HU-04)."""

    def __init__(self, numero_ticket: str):
        self.numero_ticket = numero_ticket
        super().__init__(
            "El número de ticket ingresado no existe en el sistema. "
            "Verifique el comprobante."
        )


class VentaYaEnCambioError(DomainException):
    """Se lanza cuando se intenta marcar en cambio una venta que ya está EN_CAMBIO (HU-04)."""

    def __init__(self, numero_ticket: str):
        self.numero_ticket = numero_ticket
        super().__init__(
            f"El ticket '{numero_ticket}' ya está en proceso de cambio "
            "por otra caja."
        )


class CambioInvalidoError(DomainException):
    """Se lanza cuando los datos del cambio son inválidos."""

    def __init__(self, motivo: str):
        self.motivo = motivo
        super().__init__(f"Cambio inválido: {motivo}")


class ProductoNoAptoError(DomainException):
    """Se lanza cuando el producto físico no cumple las condiciones para el cambio (HU-03)."""

    def __init__(self, motivo: str):
        self.motivo = motivo
        super().__init__(
            "El producto no cumple las condiciones para ser cambiado "
            f"(Motivo: {motivo})."
        )


class ObservacionesRequeridasError(DomainException):
    """Se lanza cuando un producto no apto se rechaza sin registrar observaciones (HU-03)."""

    def __init__(self) -> None:
        super().__init__(
            "Las observaciones son obligatorias cuando el producto no es apto "
            "para el cambio."
        )


# ── Excepciones de Autenticación (HU-09) ─────────────────────────────


class CredencialesInvalidasError(DomainException):
    """Se lanza cuando el email o la contraseña son incorrectos."""

    def __init__(self) -> None:
        super().__init__("Credenciales inválidas. Verifique email y contraseña.")


class UsuarioNoAutenticadoError(DomainException):
    """Se lanza cuando se intenta acceder a un recurso sin sesión válida."""

    def __init__(self) -> None:
        super().__init__(
            "Usuario no autenticado. Inicie sesión para continuar."
        )


class UsuarioNoAutorizadoError(DomainException):
    """Se lanza cuando el usuario autenticado no tiene el rol requerido."""

    def __init__(self, rol_requerido: str) -> None:
        self.rol_requerido = rol_requerido
        super().__init__(
            f"No tiene permisos para realizar esta acción. "
            f"Se requiere rol: {rol_requerido}."
        )


class EmailDuplicadoError(DomainException):
    """Se lanza cuando se intenta registrar un email que ya existe."""

    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"El email '{email}' ya está registrado en el sistema.")


class TokenInvalidoError(DomainException):
    """Se lanza cuando un token JWT es inválido o está expirado."""

    def __init__(self, motivo: str = "Token inválido o expirado") -> None:
        super().__init__(motivo)
