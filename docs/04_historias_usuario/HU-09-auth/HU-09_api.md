# HU-09: Especificación de API (Autenticación JWT)

**Estado**: Implementado. Los 3 endpoints funcionan y están documentados en `/api/docs`.

## Endpoint 1: Registrar Usuario
- **Método**: `POST`
- **Ruta**: `/api/v1/auth/registro`
- **Descripción**: Registra un usuario nuevo en el sistema.
- **Auth**: Requerida — solo rol `GERENTE` (via `RequireRole(RolUsuario.GERENTE)`)
- **Request Body**:
  ```json
  {
    "email": "usuario@benn.com",
    "password": "mi_password_123",
    "nombre": "Juan Pérez",
    "rol": "VENDEDOR"
  }
  ```
- **Respuesta Éxito (201 Created)**:
  ```json
  {
    "id": "uuid-123",
    "email": "usuario@benn.com",
    "nombre": "Juan Pérez",
    "rol": "VENDEDOR",
    "activo": true
  }
  ```
- **Respuesta Error (409 Conflict)**:
  ```json
  {
    "error": "EMAIL_DUPLICADO",
    "mensaje": "El email 'usuario@benn.com' ya está registrado en el sistema."
  }
  ```

## Endpoint 2: Login
- **Método**: `POST`
- **Ruta**: `/api/v1/auth/login`
- **Descripción**: Autentica un usuario y devuelve tokens de acceso.
- **Auth**: No requerida
- **Request Body**:
  ```json
  {
    "email": "usuario@benn.com",
    "password": "mi_password_123"
  }
  ```
- **Respuesta Éxito (200 OK)**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 900
  }
  ```
- **Respuesta Error (401 Unauthorized)**:
  ```json
  {
    "error": "CREDENCIALES_INVALIDAS",
    "mensaje": "Credenciales inválidas. Verifique email y contraseña."
  }
  ```

## Endpoint 3: Refresh Token
- **Método**: `POST`
- **Ruta**: `/api/v1/auth/refresh`
- **Descripción**: Renueva el access token usando un refresh token válido.
- **Auth**: No requerida (usa refresh token en body)
- **Request Body**:
  ```json
  {
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
  }
  ```
- **Respuesta Éxito (200 OK)**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 900
  }
  ```
- **Respuesta Error (401 Unauthorized)**:
  ```json
  {
    "error": "TOKEN_INVALIDO",
    "mensaje": "Token inválido o expirado"
  }
  ```

## Headers de autenticación (endpoints protegidos)

Todos los endpoints protegidos requieren el header:
```
Authorization: Bearer <access_token>
```

## Endpoints protegidos

| Endpoint | Auth requerido | Notas |
|----------|---------------|-------|
| `GET /api/v1/productos/buscar` | `get_current_user` | |
| `GET /api/v1/productos/{codigo}/stock` | `get_current_user` | |
| `POST /api/v1/ventas` | `get_current_user` | |
| `GET /api/v1/ventas/validar-ticket/{numero_ticket}` | `get_current_user` | |
| `PATCH /api/v1/ventas/{numero_ticket}/estado` | `get_current_user` | |
| `POST /api/v1/cambios` | `get_current_user` | |
| `POST /api/v1/cambios/{cambio_id}/validar-estado` | `get_current_user` | |
| `POST /api/v1/descuentos` | `get_current_user` | |
| `GET /api/v1/dashboard/resumen` | `get_current_user` | |
| `GET /api/v1/dashboard/productos-stock-bajo` | `get_current_user` | |

## Mapeo de excepciones a HTTP

| Excepción | HTTP Status | Código de error |
|-----------|-------------|-----------------|
| `CredencialesInvalidasError` | 401 | `CREDENCIALES_INVALIDAS` |
| `UsuarioNoAutenticadoError` | 401 | `USUARIO_NO_AUTENTICADO` |
| `UsuarioNoAutorizadoError` | 403 | `USUARIO_NO_AUTORIZADO` |
| `EmailDuplicadoError` | 409 | `EMAIL_DUPLICADO` |
| `TokenInvalidoError` | 401 | `TOKEN_INVALIDO` |

## Endpoints del frontend (consumidos)

| Endpoint backend | Servicio frontend | Página |
|-----------------|-------------------|--------|
| `POST /auth/login` | `authService.login()` | `LoginPage` |
| `POST /auth/registro` | `authService.registro()` | `RegisterPage` |
| `POST /auth/refresh` | `authService.refresh()` | (interceptor Axios) |
| `GET /dashboard/resumen` | `dashboardService.obtenerResumen()` | `DashboardPage` |
| `GET /dashboard/productos-stock-bajo` | `dashboardService.obtenerProductosStockBajo()` | `DashboardPage` |
