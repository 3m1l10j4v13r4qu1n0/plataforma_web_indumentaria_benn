---
tags:
  - proyecto/sgvir
  - area/backend
  - area/frontend
  - tipo/tag-trello
  - stack/fastapi
  - stack/sqlalchemy
  - stack/react
  - stack/postgresql
status: hecho
prioridad: alta
relacionado:
  - "[[Categoria - autenticacion]]"
fecha_creacion: 2026-08-26
fecha_finalizacion: 2026-08-26
agent_context: true
resumen: "Implementar capa de autenticación JWT (access + refresh token) con roles, protegiendo todos los endpoints existentes y preparando el frontend para login."
---

# HU-09 - Autenticación JWT con roles

## Descripción

El sistema actualmente tiene autenticación JWT completa: modelo de Usuario, ORM, schemas, endpoints de auth (login, registro, refresh), y protección de endpoints con `get_current_user`. El frontend tiene `AuthContext` activo, `ProtectedRoute` con soporte de roles, navbar con logout, y todas las pantallas protegidas. Los 8 endpoints existentes en 4 routers más 2 endpoints de dashboard quedan protegidos.

## Criterios de Aceptación

- Dado que un usuario ingresa email y contraseña válidos, cuando envía el formulario de login, entonces el sistema debe devolver un access token (15min) y un refresh token (7 días).

- Dado que un usuario ingresa credenciales inválidas, cuando intenta hacer login, entonces el sistema debe responder con error 401 y mensaje "Credenciales inválidas".

- Dado que un usuario tiene un access token expirado, cuando intenta acceder a un endpoint protegido, entonces el sistema debe rechazar la petición con error 401.

- Dado que un usuario tiene un refresh token válido, cuando solicita renovar el access token, entonces el sistema debe devolver un nuevo access token.

- Dado que un usuario intenta acceder a un endpoint que requiere un rol específico, cuando no tiene ese rol, entonces el sistema debe responder con error 403.

- Dado que se registra un usuario con un email que ya existe, cuando se envía el formulario, entonces el sistema debe responder con error 409.

- Dado que un usuario está autenticado, cuando accede a cualquier endpoint existente, entonces el sistema debe validar su token automáticamente.

## Specification by Example

- Login exitoso → access + refresh token
- Login con credenciales inválidas → error 401
- Refresh token válido → nuevo access token
- Access token expirado → rechazo 401
- Rol insuficiente → rechazo 403
- Email duplicado en registro → error 409

## Backend

- [x] Crear entidad `Usuario` con enum `RolUsuario` (VENDEDOR, CAJERO, GERENTE, ENCARGADO_VENTAS)
- [x] Crear puerto `IUsuarioRepository` (buscar_por_email, crear)
- [x] Crear puerto `IPasswordHasher` (hash, verify)
- [x] Crear puerto `ITokenService` (crear_access_token, crear_refresh_token, verificar_access_token, verificar_refresh_token)
- [x] Crear excepciones de dominio: `CredencialesInvalidasError`, `UsuarioNoAutenticadoError`, `UsuarioNoAutorizadoError`, `EmailDuplicadoError`, `TokenInvalidoError`
- [x] Crear caso de uso `RegistrarUsuarioUseCase`
- [x] Crear caso de uso `LoginUseCase`
- [x] Crear caso de uso `RefreshTokenUseCase`
- [x] Crear adaptador `BcryptPasswordHasher` (bcrypt>=4.0.0)
- [x] Crear adaptador `JWTTokenService` (python-jose[cryptography]>=3.3.0)
- [x] Crear ORM `UsuarioORM` (tabla `usuarios`)
- [x] Crear repositorio `UsuarioRepository` (AsyncSession)
- [x] Crear migración Alembic para tabla `usuarios`
- [x] Crear schemas Pydantic: `RegistroRequest`, `LoginRequest`, `TokenResponse`, `RefreshRequest`, `UsuarioResponse`
- [x] Crear router `auth_router.py` (POST /registro, POST /login, POST /refresh)
- [x] Crear dependencias FastAPI: `get_current_user`, `RequireRole`, `RequireAnyRole`
- [x] Mapear excepciones auth en `handlers.py`
- [x] Registrar router auth en `main.py`
- [x] Agregar dependencias a `requirements.txt`: bcrypt, python-jose, python-multipart
- [x] Agregar variables de entorno: `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`
- [x] Proteger 10 endpoints existentes con `Depends(get_current_user)`
- [x] Descomentar import de modelos ORM en `alembic/env.py`
- [x] Crear script `scripts/seed_admin.py` para usuario GERENTE inicial

## Frontend

- [x] Crear servicio `src/api/services/auth.service.ts` (login, registro, refresh)
- [x] Crear página `src/pages/auth/LoginPage.tsx` (formulario de login)
- [x] Crear página `src/pages/auth/RegisterPage.tsx` (registro, solo GERENTE)
- [x] Implementar `src/contexts/AuthContext.tsx` (login, logout, restore user from JWT)
- [x] Implementar `src/routes/ProtectedRoute.tsx` (con soporte `allowedRoles`)
- [x] Crear tipos `src/types/api/auth.types.ts`
- [x] Crear interceptor Axios con inyección de Bearer token
- [x] Crear `Navbar` con links de navegación + botón de logout
- [x] Crear `AppLayout` con navbar para rutas protegidas
- [x] Crear Dashboard (`/dashboard`) con métricas del día
- [x] Proteger rutas con roles (`/registro` solo GERENTE)
- [x] Eliminar link "Continuar sin sesión" (causaba loop infinito)
- [x] Fix 404 usando `<Link>` en vez de `<a href>`

## Notas de implementación

- La tabla de endpoints oficiales está en `fe-architect-scaffold/SKILL.md`.
- El health check real es `GET /` (no `/health`).
- Auth en el router de registro se protege con `dependencies=[Depends(RequireRole(RolUsuario.GERENTE))]`.
- Los endpoints de dashboard (`/dashboard/resumen`, `/dashboard/productos-stock-bajo`) se agregaron como parte de la mejora de navegación.
