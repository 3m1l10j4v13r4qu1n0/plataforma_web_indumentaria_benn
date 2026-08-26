# HU-09: Caso de Uso Expandido (Autenticación JWT)

**Estado**: Implementado.

**Actor Principal**: Cualquier usuario del sistema (Vendedor, Cajero, Gerente, Encargado de Ventas)
**Precondición**: El usuario tiene credenciales registradas en el sistema (o necesita registrarse).

## Flujo Principal — Login (Éxito)
1. El usuario accede a la pantalla de login (`/login`).
2. El usuario ingresa email y contraseña.
3. El sistema valida las credenciales contra la base de datos (verifica hash bcrypt).
4. El sistema genera un access token (15min) y un refresh token (7 días).
5. El sistema almacena los tokens en el `AuthContext` del frontend (localStorage + estado).
6. El sistema redirige al usuario al Dashboard (`/dashboard`).

## Flujo Alternativo 1 — Credenciales inválidas (Rechazo)
1. (Pasos 1-2 del flujo principal).
2. El sistema detecta que el email no existe o la contraseña no coincide.
3. El sistema muestra un mensaje de error: "Credenciales inválidas. Verifique email y contraseña".
4. El formulario permanece habilitado para reintento.

## Flujo Alternativo 2 — Token expirado (Refresh automático)
1. El usuario tiene un access token expirado pero refresh token válido.
2. El interceptor Axios detecta error 401 en una petición.
3. El sistema envía automáticamente una petición a `/api/v1/auth/refresh` con el refresh token.
4. El sistema recibe un nuevo access token.
5. El sistema reintenta la petición original con el nuevo token.

## Flujo Alternativo 3 — Refresh token expirado (Re-login)
1. El interceptor Axios detecta error 401 y el refresh token también falla.
2. El sistema limpia los tokens del `AuthContext` (localStorage + estado).
3. El sistema redirige al usuario a `/login`.
4. El usuario debe iniciar sesión nuevamente.

## Flujo Alternativo 4 — Registro de usuario nuevo (solo GERENTE)
1. Un usuario con rol GERENTE accede a la pantalla de registro (`/registro`).
2. El sistema valida que el usuario tenga rol GERENTE (a nivel de ruta con `allowedRoles`).
3. El usuario completa: email, contraseña (mínimo 6 caracteres), nombre, rol.
4. El sistema valida que el email no esté duplicado.
5. El sistema hashea la contraseña y crea el usuario.
6. El sistema muestra mensaje de éxito.

## Flujo Alternativo 5 — Acceso no autorizado (rol insuficiente)
1. Un usuario autenticado intenta acceder a una ruta que requiere un rol que no posee.
2. El `ProtectedRoute` con `allowedRoles` redirige al usuario a `/productos/stock`.
3. No se muestra error explícito (comportamiento silencioso).

## Flujo Alternativo 6 — Navegación con navbar
1. El usuario está autenticado y ve el navbar superior fijo.
2. El navbar muestra links: Dashboard, Consulta de Stock, Nueva Venta, Registrar Cambio.
3. El navbar muestra el nombre y rol del usuario.
4. El usuario puede cerrar sesión con el botón "Cerrar sesión".
5. Al cerrar sesión, se limpian los tokens y se redirige a `/login`.

## Flujo Alternativo 7 — Dashboard como página principal
1. El usuario autenticado accede a `/` o `/dashboard`.
2. El Dashboard muestra métricas del día: ventas, total facturado, productos con stock bajo.
3. El Dashboard muestra accesos rápidos a las 3 pantallas principales.
4. El Dashboard muestra la lista de productos con stock bajo (≤ 5 unidades).

## Postcondición
- El usuario autenticado puede acceder a todos los endpoints protegidos según su rol.
- Los 10 endpoints existentes quedan protegidos con `Depends(get_current_user)`.
- Los tokens se gestionan automáticamente en el frontend (interceptor Axios + AuthContext).
- El navbar permite navegar entre pantallas y cerrar sesión.
- El dashboard muestra un resumen de la operativa del día.
