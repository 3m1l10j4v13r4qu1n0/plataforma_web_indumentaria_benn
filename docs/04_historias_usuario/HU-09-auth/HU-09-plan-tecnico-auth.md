# HU-09 — Plan Técnico: Capa de Autenticación (JWT)

## 1. Contexto y Alcance

### Situación actual
- **No existe** modelo de Usuario, ORM, schema ni endpoints de auth en el backend.
- **No hay librerías de auth** en `requirements.txt`.
- El frontend tiene `AuthContext`, `ProtectedRoute` e interceptor Axios pre-armados pero **desactivados** (YAGNI).
- Hay **8 endpoints** existentes en 4 routers que deben quedar protegidos.

### Objetivo
Implementar autenticación JWT (access + refresh token) con roles, protegiendo todos los endpoints existentes y preparando el frontend para login.

### Decisiones confirmadas
| Decisión | Elección |
|----------|----------|
| Mecanismo | JWT (access + refresh token) |
| Roles | VENDEDOR, CAJERO, GERENTE, ENCARGADO_VENTAS |
| Refresh token | Sí (access: 15min, refresh: 7 días) |
| Persistencia | Tabla nueva `usuarios` en PostgreSQL |

---

## 2. Estructura de archivos nuevos

```
src/backend/app/
├── domain/
│   ├── models/
│   │   └── usuario.py                  ← Entidad Usuario
│   ├── ports/
│   │   ├── i_usuario_repository.py     ← Protocol repositorio
│   │   ├── i_password_hasher.py        ← Protocol hash
│   │   └── i_token_service.py          ← Protocol tokens
│   └── exceptions.py                   ← Agregar excepciones auth
├── application/
│   └── use_cases/
│       ├── registrar_usuario_use_case.py
│       ├── login_use_case.py
│       └── refresh_token_use_case.py
├── infrastructure/
│   ├── auth/
│   │   ├── bcrypt_password_hasher.py   ← Adaptador concreto
│   │   └── jwt_token_service.py        ← Adaptador concreto
│   ├── database/
│   │   ├── orm_models/
│   │   │   └── usuario_orm.py          ← ORM SQLAlchemy
│   │   └── repositories/
│   │       └── usuario_repository.py   ← Implementación repositorio
│   └── dependencies/
│       └── dependency_injection.py     ← Agregar fábricas auth
├── presentation/
│   ├── schemas/
│   │   └── auth_schema.py              ← Schemas Pydantic
│   ├── routers/
│   │   └── auth_router.py              ← Endpoints auth
│   ├── dependencies.py                 ← get_current_user, require_role
│   └── handlers.py                     ← Mapear excepciones auth
└── main.py                             ← Registrar router auth

src/backend/
└── requirements.txt                    ← Agregar dependencias

src/backend/alembic/versions/
└── XXXX_create_usuarios_table.py       ← Migración
```

---

## 3. Dominio — Entidad y Puertos

### 3.1 Entidad `Usuario` (`app/domain/models/usuario.py`)

```python
from dataclasses import dataclass
from enum import Enum

class RolUsuario(str, Enum):
    VENDEDOR = "VENDEDOR"
    CAJERO = "CAJERO"
    GERENTE = "GERENTE"
    ENCARGADO_VENTAS = "ENCARGADO_VENTAS"

@dataclass
class Usuario:
    id: str
    email: str
    password_hash: str
    nombre: str
    rol: RolUsuario
    activo: bool = True

    def esta_activo(self) -> bool:
        return self.activo

    def tiene_rol(self, rol: RolUsuario) -> bool:
        return self.rol == rol
```

### 3.2 Puerto `IUsuarioRepository` (`app/domain/ports/i_usuario_repository.py`)

```python
from typing import Protocol
from app.domain.models.usuario import Usuario

class IUsuarioRepository(Protocol):
    async def buscar_por_email(self, email: str) -> Usuario | None: ...
    async def crear(self, usuario: Usuario) -> Usuario: ...
```

### 3.3 Puerto `IPasswordHasher` (`app/domain/ports/i_password_hasher.py`)

```python
from typing import Protocol

class IPasswordHasher(Protocol):
    def hash(self, password: str) -> str: ...
    def verify(self, password: str, hashed: str) -> bool: ...
```

### 3.4 Puerto `ITokenService` (`app/domain/ports/i_token_service.py`)

```python
from typing import Protocol

class ITokenService(Protocol):
    def crear_access_token(self, user_id: str, rol: str) -> str: ...
    def crear_refresh_token(self, user_id: str) -> str: ...
    def verificar_access_token(self, token: str) -> dict: ...
    def verificar_refresh_token(self, token: str) -> dict: ...
```

### 3.5 Excepciones nuevas (agregar a `app/domain/exceptions.py`)

```python
class CredencialesInvalidasError(DomainException):
    def __init__(self):
        super().__init__("Credenciales inválidas. Verifique email y contraseña.")

class UsuarioNoAutenticadoError(DomainException):
    def __init__(self):
        super().__init__("Usuario no autenticado. Inicie sesión para continuar.")

class UsuarioNoAutorizadoError(DomainException):
    def __init__(self, rol_requerido: str):
        self.rol_requerido = rol_requerido
        super().__init__(
            f"No tiene permisos para realizar esta acción. "
            f"Se requiere rol: {rol_requerido}."
        )

class EmailDuplicadoError(DomainException):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"El email '{email}' ya está registrado en el sistema.")

class TokenInvalidoError(DomainException):
    def __init__(self, motivo: str = "Token inválido o expirado"):
        super().__init__(motivo)
```

---

## 4. Casos de uso

### 4.1 `RegistrarUsuarioUseCase`
- Recibe: email, password, nombre, rol
- Valida: email único (via repo), password no vacío
- Hashea password (via `IPasswordHasher`)
- Crea usuario (via `IUsuarioRepository`)
- Retorna: `Usuario` creado

### 4.2 `LoginUseCase`
- Recibe: email, password
- Busca usuario por email (via `IUsuarioRepository`)
- Verifica password (via `IPasswordHasher`)
- Genera access token + refresh token (via `ITokenService`)
- Retorna: `TokenResponse(access_token, refresh_token, token_type, expires_in)`

### 4.3 `RefreshTokenUseCase`
- Recibe: refresh token
- Verifica refresh token (via `ITokenService`)
- Extrae user_id del payload
- Genera nuevo access token
- Retorna: `TokenResponse`

---

## 5. Infraestructura — Adaptadores concretos

### 5.1 `BcryptPasswordHasher`
- Usa `bcrypt` directamente (librería nativa, más moderna que passlib)
- Implementa `IPasswordHasher`

### 5.2 `JWTTokenService`
- Usa `python-jose[cryptography]`
- Implementa `ITokenService`
- Configuración via `app/infrastructure/core/config.py`:
  - `JWT_SECRET_KEY`
  - `JWT_ALGORITHM = "HS256"`
  - `ACCESS_TOKEN_EXPIRE_MINUTES = 15`
  - `REFRESH_TOKEN_EXPIRE_DAYS = 7`

### 5.3 `UsuarioORM` (`app/infrastructure/database/orm_models/usuario_orm.py`)

```python
from sqlalchemy import Boolean, Index, String
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.session import Base

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

### 5.4 `UsuarioRepository` (`app/infrastructure/database/repositories/usuario_repository.py`)
- Implementa `IUsuarioRepository`
- Usa `AsyncSession` (patrón igual a `ProductoRepository`)

---

## 6. Endpoints

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/api/v1/auth/registro` | Registrar usuario nuevo | No |
| `POST` | `/api/v1/auth/login` | Login, devuelve tokens | No |
| `POST` | `/api/v1/auth/refresh` | Renovar access token | No (usa refresh token) |

### 6.1 Schemas Pydantic (`app/presentation/schemas/auth_schema.py`)

```python
class RegistroRequest(BaseModel):
    email: str = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=6, description="Contraseña (mínimo 6 caracteres)")
    nombre: str = Field(..., description="Nombre completo")
    rol: str = Field(..., description="Rol del usuario")

class LoginRequest(BaseModel):
    email: str = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña")

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class RefreshRequest(BaseModel):
    refresh_token: str
```

### 6.2 Dependencias de FastAPI (`app/presentation/dependencies.py`)

```python
# get_current_user: extrae Bearer token del header, verifica, retorna Usuario
# require_role(rol: RolUsuario): wrapper que valida el rol del usuario actual
```

Uso en endpoints protegidos:
```python
@router.get("/productos/buscar")
async def buscarProductos(
    use_case: ... = Depends(...),
    usuario: Usuario = Depends(get_current_user),  # Solo por agregar
):
    ...
```

---

## 7. Mapeo de excepciones en `handlers.py`

| Excepción | HTTP Status | Código de error |
|-----------|-------------|-----------------|
| `CredencialesInvalidasError` | 401 | `CREDENCIALES_INVALIDAS` |
| `UsuarioNoAutenticadoError` | 401 | `USUARIO_NO_AUTENTICADO` |
| `UsuarioNoAutorizadoError` | 403 | `USUARIO_NO_AUTORIZADO` |
| `EmailDuplicadoError` | 409 | `EMAIL_DUPLICADO` |
| `TokenInvalidoError` | 401 | `TOKEN_INVALIDO` |

---

## 8. Dependencias a agregar (`requirements.txt`)

```
bcrypt>=4.0.0,<5.0.0
python-jose[cryptography]>=3.3.0,<4.0.0
python-multipart>=0.0.9,<1.0.0
```

---

## 9. Variables de entorno (`.env.example`)

```
JWT_SECRET_KEY=CHANGE_ME_TO_A_RANDOM_SECRET
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## 10. Frontend

| Archivo | Acción |
|---------|--------|
| `src/api/services/auth.service.ts` | Crear servicio: login, registro, refresh |
| `src/pages/auth/LoginPage.tsx` | Crear formulario de login |
| `src/contexts/AuthContext.tsx` | Activar lógica comentada, conectar al backend |
| `src/routes/AppRouter.tsx` | Envolver rutas en `ProtectedRoute`, agregar `/login` |
| `src/types/api/auth.types.ts` | Tipos de la API de auth |

---

## 11. Tests

| Archivo | Qué testea |
|---------|------------|
| `tests/unit/use_cases/test_registrar_usuario.py` | Registro exitoso, email duplicado, password corto |
| `tests/unit/use_cases/test_login.py` | Login exitoso, credenciales inválidas |
| `tests/unit/use_cases/test_refresh_token.py` | Refresh exitoso, token inválido/expirado |
| `tests/unit/auth/test_password_hasher.py` | Hash y verify con bcrypt |
| `tests/unit/auth/test_token_service.py` | Crear y verificar tokens JWT |

Todos los tests usan **fakes en memoria** (sin DB), siguiendo el patrón de `tests/unit/fakes/`.

---

## 12. Orden de ejecución

| Paso | Fase | Archivos | Dependencias |
|------|------|----------|-------------|
| 1 | Dominio | `usuario.py`, puertos, excepciones | Ninguna |
| 2 | Casos de uso | 3 use cases | Paso 1 |
| 3 | Infraestructura | ORM, repos, adaptadores, config | Paso 1 |
| 4 | Migración | Alembic | Paso 3 |
| 5 | Endpoints | schemas, router, dependencies, handlers | Pasos 2-4 |
| 6 | Tests | Tests unitarios | Pasos 1-5 |
| 7 | Proteger endpoints | Agregar `Depends(get_current_user)` a 4 routers | Paso 5 |
| 8 | Frontend | auth.service, LoginPage, AuthContext activado | Paso 5 |

---

## 13. Riesgos y consideraciones

1. **`alembic/env.py`**: Actualmente NO importa los modelos ORM (línea comentada). Hay que descomentar/agregar el import de `UsuarioORM` para que autogenerate detecte la tabla nueva.
2. **`python-multipart`**: FastAPI lo necesita para formularios, pero no está en `requirements.txt`. Hay que agregarlo.
3. **Seed de usuario admin**: Para testing inicial, Considerar un script que cree un usuario GERENTE de prueba.
4. **CORS**: Verificar que el frontend en puerto 5173 pueda hacer requests al backend en puerto 8000 con credenciales.
