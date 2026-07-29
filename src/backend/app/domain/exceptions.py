class DomainException(Exception):
    """Excepción base para todas las excepciones de dominio."""

    pass


class ProductoNoEncontradoError(DomainException):
    """Se lanza cuando se intenta operar con un producto que no existe."""

    def __init__(self, codigo: str):
        self.codigo = codigo
        self.producto_id = codigo
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


class CategoriaInvalidaError(DomainException):
    """Se lanza cuando los datos de una categoría no cumplen sus invariantes."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje)


class CategoriaNoEncontradaError(DomainException):
    """Se lanza cuando se referencia una categoría que no existe."""

    def __init__(self, categoria_id: int):
        self.categoria_id = categoria_id
        super().__init__(
            f"No se encontró la categoría con id '{categoria_id}'."
        )


class CategoriaYaExisteError(DomainException):
    """Se lanza cuando se intenta crear una categoría con un nombre ya existente."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        super().__init__(
            f"Ya existe una categoría con el nombre '{nombre}'."
        )
