# Documentación Técnica: Registro de Usuario

## 1. Resumen del Caso de Uso
El caso de uso **RegistrarUsuario** permite dar de alta nuevos usuarios en el sistema. Garantiza la unicidad del correo electrónico y asegura que la contraseña sea almacenada de forma segura (hasheada con bcrypt) antes de persistir los datos.

## 2. Precondiciones
- El usuario que realiza la petición debe tener el rol **GERENTE**.
- El dominio `Usuario` y sus puertos (`IUsuarioRepository`, `IPasswordHasher`) deben estar correctamente implementados.

## 3. Arquitectura y Capas

### 3.1. Entidad de Dominio (`app/domain/models/usuario.py`)
Representa al usuario con los siguientes atributos:
- `id` (str): Identificador único (UUID).
- `email` (str): Correo electrónico único.
- `password_hash` (str): Contraseña hasheada (nunca se almacena en texto plano).
- `nombre` (str): Nombre completo.
- `rol` (RolUsuario): Enum con roles (`VENDEDOR`, `CAJERO`, `GERENTE`, `ENCARGADO_VENTAS`).
- `activo` (bool): Estado de la cuenta (por defecto `True`).

### 3.2. Puertos (Interfaces)
- **`IUsuarioRepository`**: Define los métodos `buscar_por_email` y `crear`.
- **`IPasswordHasher`**: Define el método `hash` para el procesamiento de contraseñas.

### 3.3. Caso de Uso (`app/application/use_cases/registrar_usuario_use_case.py`)
Flujo interno:
1.  Verifica si el email ya existe en el repositorio. Si existe, lanza `EmailDuplicadoError`.
2.  Hashea la contraseña utilizando el puerto `IPasswordHasher`.
3.  Instancia la entidad `Usuario` con un nuevo UUID.
4.  Persiste el usuario mediante el repositorio.

### 3.4. Endpoints (`app/presentation/routers/auth_router.py`)
- **Ruta**: `POST /api/v1/auth/registro`
- **Autenticación**: Requiere token JWT con rol `GERENTE`.
- **Entrada**: `RegistroRequest` (email, password, nombre, rol).
- **Salida**: `UsuarioResponse` (id, email, nombre, rol, activo).
- **Códigos de Respuesta**:
    - `201 Created`: Registro exitoso.
    - `409 Conflict`: Email duplicado (`EmailDuplicadoError`).
    - `401 Unauthorized`: Credenciales inválidas o falta de token.
    - `403 Forbidden`: Rol insuficiente.

## 4. Schemas Pydantic (`app/presentation/schemas/auth_schema.py`)
```python
class RegistroRequest(BaseModel):
    email: str
    password: str = Field(..., min_length=6)
    nombre: str
    rol: str

class UsuarioResponse(BaseModel):
    id: str
    email: str
    nombre: str
    rol: str
    activo: bool
```

## 5. Excepciones de Dominio
- `EmailDuplicadoError`: Se activa cuando se intenta registrar un email existente.

## 6. Dependency Injection
El punto de ensamblaje se encuentra en `app/infrastructure/dependencies/dependency_injection.py`, donde se conecta la implementación concreta del repositorio y el hasher al caso de uso.
