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


# HU-02 exceptions


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
