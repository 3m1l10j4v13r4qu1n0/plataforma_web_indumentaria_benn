# HU-09: Modelos de Datos (Autenticación JWT)

## Entidades Involucradas

### 1. Usuario (Nueva)
- `id` (String/UUID): Identificador único.
- `email` (String): Email del usuario (único, índice de búsqueda).
- `password_hash` (String): Contraseña hasheada con bcrypt.
- `nombre` (String): Nombre completo del usuario.
- `rol` (Enum/String): Rol del usuario — `VENDEDOR` | `CAJERO` | `GERENTE` | `ENCARGADO_VENTAS`.
- `activo` (Boolean): Si el usuario está habilitado. Default `true`.

### 2. Roles del sistema
| Rol | Descripción |
|-----|-------------|
| `VENDEDOR` | Realiza ventas, consulta stock |
| `CAJERO` | Procesa pagos, emite tickets |
| `GERENTE` | Administra descuentos, autoriza operaciones |
| `ENCARGADO_VENTAS` | Supervisa operaciones de venta |

## Puertos (Interfaces de dominio)

### `IUsuarioRepository`
- `buscar_por_email(email: str) → Usuario | None`
- `crear(usuario: Usuario) → Usuario`

### `IPasswordHasher`
- `hash(password: str) → str`
- `verify(password: str, hashed: str) → bool`

### `ITokenService`
- `crear_access_token(user_id: str, rol: str) → str`
- `crear_refresh_token(user_id: str) → str`
- `verificar_access_token(token: str) → dict`
- `verificar_refresh_token(token: str) → dict`

## ORM — `UsuarioORM`

```python
class UsuarioORM(Base):
    __tablename__ = "usuarios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    rol: Mapped[str] = mapped_column(String(30), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __table_args__ = (
        Index("ix_usuario_email", "email"),
    )
```

## Reglas de Integridad y Base de Datos

- El campo `email` debe tener restricción `UNIQUE` e índice para búsquedas rápidas.
- El campo `rol` debe ser un string de máximo 30 caracteres (los valores del enum se almacenan como string).
- La contraseña NUNCA se almacena en texto plano; solo el hash bcrypt.
- La tabla `usuarios` se crea mediante migración Alembic.
- **Nota**: `alembic/env.py` NO importa los modelos ORM actualmente (línea comentada). Hay que descomentar/agregar el import de `UsuarioORM` para que autogenerate detecte la tabla nueva.

## Dependencias a agregar (`requirements.txt`)

```
bcrypt>=4.0.0,<5.0.0
python-jose[cryptography]>=3.3.0,<4.0.0
python-multipart>=0.0.9,<1.0.0
```

## Variables de entorno (`.env.example`)

```
JWT_SECRET_KEY=CHANGE_ME_TO_A_RANDOM_SECRET
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```
