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
status: pendiente
prioridad: alta
relacionado:
  - "[[Categoria - autenticacion]]"
fecha_creacion: 2026-08-26
agent_context: true
resumen: "Implementar capa de autenticación JWT (access + refresh token) con roles, protegiendo todos los endpoints existentes y preparando el frontend para login."
---

# HU-09 - Autenticación JWT con roles

## Descripción

El sistema actualmente no tiene autenticación: no existe modelo de Usuario, ORM, schema ni endpoints de auth. El frontend tiene `AuthContext`, `ProtectedRoute` e interceptor Axios pre-armados pero desactivados. Hay 8 endpoints existentes en 4 routers que deben quedar protegidos. Se implementará autenticación JWT (access + refresh token) con roles para controlar el acceso a todo el sistema.

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

## Acceptance TDD

- Probar login exitoso con credenciales correctas
- Probar login fallido con credenciales incorrectas
- Probar refresh token exitoso
- Probar refresh token inválido/expirado
- Probar protección de endpoints con token válido
- Probar rechazo de endpoints sin token
- Probar registro exitoso
- Probar registro con email duplicado

## Backend

- [ ] Crear entidad `Usuario` con enum `RolUsuario` (VENDEDOR, CAJERO, GERENTE, ENCARGADO_VENTAS)
- [ ] Crear puerto `IUsuarioRepository` (buscar_por_email, crear)
- [ ] Crear puerto `IPasswordHasher` (hash, verify)
- [ ] Crear puerto `ITokenService` (crear_access_token, crear_refresh_token, verificar_access_token, verificar_refresh_token)
- [ ] Crear excepciones de dominio: `CredencialesInvalidasError`, `UsuarioNoAutenticadoError`, `UsuarioNoAutorizadoError`, `EmailDuplicadoError`, `TokenInvalidoError`
- [ ] Crear caso de uso `RegistrarUsuarioUseCase`
- [ ] Crear caso de uso `LoginUseCase`
- [ ] Crear caso de uso `RefreshTokenUseCase`
- [ ] Crear adaptador `BcryptPasswordHasher` (bcrypt>=4.0.0)
- [ ] Crear adaptador `JWTTokenService` (python-jose[cryptography]>=3.3.0)
- [ ] Crear ORM `UsuarioORM` (tabla `usuarios`)
- [ ] Crear repositorio `UsuarioRepository` (AsyncSession)
- [ ] Crear migración Alembic para tabla `usuarios`
- [ ] Crear schemas Pydantic: `RegistroRequest`, `LoginRequest`, `TokenResponse`, `RefreshRequest`
- [ ] Crear router `auth_router.py` (POST /registro, POST /login, POST /refresh)
- [ ] Crear dependencias FastAPI: `get_current_user`, `require_role`
- [ ] Mapear excepciones auth en `handlers.py`
- [ ] Registrar router auth en `main.py`
- [ ] Agregar dependencias a `requirements.txt`: bcrypt, python-jose, python-multipart
- [ ] Agregar variables de entorno: `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`
- [ ] Proteger 8 endpoints existentes con `Depends(get_current_user)`
- [ ] Descomentar import de modelos ORM en `alembic/env.py`

## Frontend

- [ ] Crear servicio `src/api/services/auth.service.ts` (login, registro, refresh)
- [ ] Crear página `src/pages/auth/LoginPage.tsx` (formulario de login)
- [ ] Activar lógica de `src/contexts/AuthContext.tsx` (conectar al backend)
- [ ] Modificar `src/routes/AppRouter.tsx` (envolver rutas en `ProtectedRoute`, agregar `/login`)
- [ ] Crear tipos `src/types/api/auth.types.ts`
