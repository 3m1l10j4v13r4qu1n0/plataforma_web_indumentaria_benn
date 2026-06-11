"""
Pruebas de Aislamiento (Testing) HU-05
Repositorio Falso de Usuario

"""

from app.domain.ports.i_usuario_repository import IUsuarioRepository


class FakeUsuarioRepository(IUsuarioRepository):
    def __init__(self):
        # Diccionario simple: usuario_id -> rol
        self._usuarios = {
            "GERENTE-001": "GERENTE",
            "VENDEDOR-001": "VENDEDOR",
            "CAJERO-001": "CAJERO",
        }

    def agregar_usuario(self, usuario_id: str, rol: str):
        self._usuarios[usuario_id] = rol

    async def es_gerente(self, usuario_id: str) -> bool:
        rol = self._usuarios.get(usuario_id, "")
        return rol.upper() == "GERENTE"
