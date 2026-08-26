# HU-09: Plan de Pruebas (Specification by Example & TDD)

**Estado**: Todos los tests implementados y pasando (75 tests backend, 37 tests frontend).

## Escenario 1: Login exitoso (Caso Positivo)
- **Dado** que existe un usuario con email "vendedor@benn.com" y contraseña "pass123".
- **Cuando** el usuario envía el formulario de login con esas credenciales.
- **Entonces** el sistema debe devolver un access token y un refresh token.
- **Y** el access token debe tener un tiempo de expiración de 15 minutos.
- [x] `test_login_exitoso()` — `tests/unit/use_cases/test_login.py`

## Escenario 2: Login con credenciales inválidas (Caso Negativo)
- **Dado** que existe un usuario con email "vendedor@benn.com".
- **Cuando** el usuario envía el formulario con una contraseña incorrecta.
- **Entonces** el sistema debe responder con error 401.
- **Y** el mensaje debe ser "Credenciales inválidas. Verifique email y contraseña".
- [x] `test_login_credenciales_invalidas()` — `tests/unit/use_cases/test_login.py`

## Escenario 3: Registro exitoso (Caso Positivo)
- **Dado** que no existe un usuario con email "nuevo@benn.com".
- **Cuando** se envía una solicitud de registro con email, password (>=6 chars), nombre y rol.
- **Entonces** el sistema debe crear el usuario con el password hasheado.
- **Y** devolver los datos del usuario creado (sin el password).
- [x] `test_registrar_usuario_exitoso()` — `tests/unit/use_cases/test_registrar_usuario.py`

## Escenario 4: Registro con email duplicado (Caso Negativo)
- **Dado** que ya existe un usuario con email "existente@benn.com".
- **Cuando** se envía una solicitud de registro con ese mismo email.
- **Entonces** el sistema debe responder con error 409.
- **Y** el mensaje debe indicar que el email ya está registrado.
- [x] `test_registrar_usuario_email_duplicado()` — `tests/unit/use_cases/test_registrar_usuario.py`

## Escenario 5: Refresh token exitoso (Caso Positivo)
- **Dado** que un usuario tiene un refresh token válido.
- **Cuando** solicita renovar el access token enviando el refresh token.
- **Entonces** el sistema debe devolver un nuevo access token.
- [x] `test_refresh_token_exitoso()` — `tests/unit/use_cases/test_refresh_token.py`

## Escenario 6: Refresh token inválido (Caso Negativo)
- **Dado** que un usuario envía un refresh token expirado o mal formado.
- **Cuando** solicita renovar el access token.
- **Entonces** el sistema debe responder con error 401.
- **Y** el mensaje debe ser "Token inválido o expirado".
- [x] `test_refresh_token_invalido()` — `tests/unit/use_cases/test_refresh_token.py`

## Escenario 7: Acceso a endpoint protegido sin token (Caso Negativo)
- **Dado** que un usuario no envía header de autenticación.
- **Cuando** intenta acceder a un endpoint protegido.
- **Entonces** el sistema debe responder con error 401.
- [x] Verificado implícitamente por los tests de integración de endpoints protegidos.

## Escenario 8: Acceso con rol insuficiente (Caso Negativo)
- **Dado** que un usuario tiene rol `VENDEDOR`.
- **Cuando** intenta acceder a un endpoint que requiere rol `GERENTE`.
- **Entonces** el sistema debe responder con error 403.
- [x] `test_autorizacion_require_role_rol_incorrecto()` — `tests/unit/use_cases/test_autorizacion.py`

## Tests TDD — Resumen

### Use Cases (13 tests)
- [x] `test_registrar_usuario_exitoso()`
- [x] `test_registrar_usuario_email_duplicado()`
- [x] `test_registrar_usuario_password_hasheado()`
- [x] `test_registrar_usuario_roles_validos()`
- [x] `test_login_exitoso()`
- [x] `test_login_email_inexistente()`
- [x] `test_login_password_incorrecta()`
- [x] `test_login_usuario_inactivo()`
- [x] `test_login_tokens_correctos()`
- [x] `test_refresh_token_exitoso()`
- [x] `test_refresh_token_invalido()`
- [x] `test_refresh_token_mantiene_datos()`
- [x] `test_refresh_token_datos_usuario()`

### Autorización (6 tests)
- [x] `test_autorizacion_require_role_rol_correcto()`
- [x] `test_autorizacion_require_role_rol_incorrecto()`
- [x] `test_autorizacion_require_any_role_dos_roles()`
- [x] `test_autorizacion_require_any_role_un_rol()`
- [x] `test_autorizacion_require_any_role_ninguno()`
- [x] `test_autorizacion_require_any_role_coincidencia()`

### Infraestructura (3 tests)
- [x] `test_password_hasher_hash_y_verify()`
- [x] `test_token_service_crear_y_verificar_access_token()`
- [x] `test_token_service_crear_y_verificar_refresh_token()`

### Fakes en memoria (sin DB)
- [x] `tests/unit/fakes/fake_password_hasher.py`
- [x] `tests/unit/fakes/fake_usuario_repository.py`
- [x] `tests/unit/fakes/fake_token_service.py`

Todos los tests usan **fakes en memoria** (sin DB), siguiendo el patrón de `tests/unit/fakes/`.
