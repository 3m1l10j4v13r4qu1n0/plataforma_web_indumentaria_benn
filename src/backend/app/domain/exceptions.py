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


class ProductoInvalidoError(DomainException):
    """Se lanza cuando el producto no está en estado ACTIVO."""

    def __init__(self, producto_id: str, estado: str):
        self.producto_id = producto_id
        self.estado = estado
        super().__init__(
            f"El producto con ID '{producto_id}' no está activo (Estado: {estado})."
        )
