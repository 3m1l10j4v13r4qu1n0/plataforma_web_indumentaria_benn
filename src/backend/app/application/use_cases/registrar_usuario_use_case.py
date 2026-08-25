import uuid

from app.domain.exceptions import EmailDuplicadoError
from app.domain.models.usuario import RolUsuario, Usuario
from app.domain.ports.i_password_hasher import IPasswordHasher
from app.domain.ports.i_usuario_repository import IUsuarioRepository


class RegistrarUsuarioUseCase:
    """Caso de uso para registrar un nuevo usuario en el sistema.

    Valida que el email no esté duplicado, hashea la contraseña
    y persiste el usuario en la base de datos.
    """

    def __init__(
        self,
        usuario_repository: IUsuarioRepository,
        password_hasher: IPasswordHasher,
    ):
        self._usuario_repository = usuario_repository
        self._password_hasher = password_hasher

    async def execute(
        self, email: str, password: str, nombre: str, rol: RolUsuario
    ) -> Usuario:
        """Registra un usuario nuevo.

        Args:
            email: Email único del usuario.
            password: Contraseña en texto plano (se hasheará).
            nombre: Nombre completo del usuario.
            rol: Rol asignado al usuario.

        Returns:
            Usuario creado con ID generado.

        Raises:
            EmailDuplicadoError: Si el email ya está registrado.
        """
        existente = await self._usuario_repository.buscar_por_email(email)
        if existente is not None:
            raise EmailDuplicadoError(email)

        password_hash = self._password_hasher.hash(password)

        usuario = Usuario(
            id=str(uuid.uuid4()),
            email=email,
            password_hash=password_hash,
            nombre=nombre,
            rol=rol,
            activo=True,
        )

        return await self._usuario_repository.crear(usuario)
