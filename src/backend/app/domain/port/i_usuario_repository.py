from typing import Protocol


class IUsuarioRepository(Protocol):
    async def es_gerente(self, usuario_id: str) -> bool:
        """
        Verifica si el usuario tiene el rol de Gerente para autorizar excepciones.
        """
        ...
