class FakeGeneradorNumeroTicket:
    """Fake en memoria del generador de números de ticket.

    Entrega números secuenciales deterministas (T-TEST-001, T-TEST-002, ...)
    y registra los generados para poder asertar sobre ellos.
    """

    def __init__(self):
        self._secuencia = 0
        self.generados: list[str] = []

    async def generar(self) -> str:
        self._secuencia += 1
        numero = f"T-TEST-{self._secuencia:03d}"
        self.generados.append(numero)
        return numero
