# HU-09: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Login exitoso (Caso Positivo)
- **Dado** que existe un usuario con email "vendedor@benn.com" y contraseña "pass123".
- **Cuando** el usuario envía el formulario de login con esas credenciales.
- **Entonces** el sistema debe devolver un access token y un refresh token.
- **Y** el access token debe tener un tiempo de expiración de 15 minutos.

## Escenario 2: Login con credenciales inválidas (Caso Negativo)
- **Dado** que existe un usuario con email "vendedor@benn.com".
- **Cuando** el usuario envía el formulario con una contraseña incorrecta.
- **Entonces** el sistema debe responder con error 401.
- **Y** el mensaje debe ser "Credenciales inválidas. Verifique email y contraseña".

## Escenario 3: Registro exitoso (Caso Positivo)
- **Dado** que no existe un usuario con email "nuevo@benn.com".
- **Cuando** se envía una solicitud de registro con email, password (>=6 chars), nombre y rol.
- **Entonces** el sistema debe crear el usuario con el password hasheado.
- **Y** deveolver los datos del usuario creado (sin el password).

## Escenario 4: Registro con email duplicado (Caso Negativo)
- **Dado** que ya existe un usuario con email "existente@benn.com".
- **Cuando** se envía una solicitud de registro con ese mismo email.
- **Entonces** el sistema debe responder con error 409.
- **Y** el mensaje debe indicar que el email ya está registrado.

## Escenario 5: Refresh token exitoso (Caso Positivo)
- **Dado** que un usuario tiene un refresh token válido.
- **Cuando** solicita renovar el access token enviando el refresh token.
- **Entonces** el sistema debe devolver un nuevo access token.

## Escenario 6: Refresh token inválido (Caso Negativo)
- **Dado** que un usuario envía un refresh token expirado o mal formado.
- **Cuando** solicita renovar el access token.
- **Entonces** el sistema debe responder con error 401.
- **Y** el mensaje debe ser "Token inválido o expirado".

## Escenario 7: Acceso a endpoint protegido sin token (Caso Negativo)
- **Dado** que un usuario no envía header de autenticación.
- **Cuando** intenta acceder a un endpoint protegido.
- **Entonces** el sistema debe responder con error 401.

## Escenario 8: Acceso con rol insuficiente (Caso Negativo)
- **Dado** que un usuario tiene rol `VENDEDOR`.
- **Cuando** intenta acceder a un endpoint que requiere rol `GERENTE`.
- **Entonces** el sistema debe responder con error 403.

## Casos de Prueba TDD (Checklist para Desarrolladores)

### Use Cases
- [ ] `test_registrar_usuario_exitoso()`
- [ ] `test_registrar_usuario_email_duplicado()`
- [ ] `test_registrar_usuario_password_corto()`
- [ ] `test_login_exitoso()`
- [ ] `test_login_credenciales_invalidas()`
- [ ] `test_refresh_token_exitoso()`
- [ ] `test_refresh_token_invalido()`

### Infraestructura
- [ ] `test_password_hasher_hash_y_verify()`
- [ ] `test_token_service_crear_y_verificar_access_token()`
- [ ] `test_token_service_crear_y_verificar_refresh_token()`
- [ ] `test_token_service_token_expirado()`

### Endpoints (integración)
- [ ] `test_endpoint_registro_201()`
- [ ] `test_endpoint_registro_409_email_duplicado()`
- [ ] `test_endpoint_login_200()`
- [ ] `test_endpoint_login_401()`
- [ ] `test_endpoint_refresh_200()`
- [ ] `test_endpoint_protegido_401_sin_token()`
- [ ] `test_endpoint_protegido_403_rol_insuficiente()`

Todos los tests usan **fakes en memoria** (sin DB), siguiendo el patrón de `tests/unit/fakes/`.
