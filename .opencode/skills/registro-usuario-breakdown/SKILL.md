---
name: registro-usuario-breakdown
description: >
  Implementa el caso de uso de registro de usuarios (RegistrarUsuarioUseCase)
  dentro de la capa de autenticación, con verificación obligatoria del
  dominio real (entidad Usuario, repositorio, puerto de hashing) antes de
  escribir código. Usar cuando el usuario pida crear, modificar o revisar
  el registro/alta de usuarios, validación de email único o de contraseña.
disable-model-invocation: true
---

# registro-usuario-breakdown

## Propósito

Guiar la implementación del registro de usuarios como parte de
`feature/auth-autenticacion`, sin inventar campos de la entidad
`Usuario`, firmas del repositorio, ni reglas de validación que no
estén confirmadas por el código real o por el usuario.

Depende de que ya exista (o se defina en el mismo hilo de trabajo):
- La entidad `Usuario` del dominio.
- El repositorio de `Usuario` (puerto + adaptador).
- `IPasswordHasher` (ya implementado con `bcrypt`, ver capa de auth).

## Regla de oro

> Si no leíste la entidad `Usuario` ni el repositorio en esta sesión,
> no armes el caso de uso todavía. Pedilos primero.

No asumir nombres como `email`, `password_hash`, `obtener_por_email`,
`guardar`, etc. — pedir el código real y usar los nombres exactos que
aparezcan ahí.

## Precondiciones (verificar antes de escribir el caso de uso)

1. Leer la entidad `Usuario` completa: campos, validaciones internas,
   si ya tiene un método de factory (`Usuario.crear(...)`) o si se
   instancia directo.
2. Leer la interfaz del repositorio (`UsuarioRepositoryPort` o el
   nombre que use el proyecto): confirmar el método exacto para buscar
   por email (¿`obtener_por_email`? ¿`buscar_por_email`? ¿devuelve
   `Usuario | None` o lanza excepción si no existe?) y el método para
   persistir (¿`guardar`? ¿`crear`?).
3. Confirmar si ya existe un DTO/schema de entrada (Pydantic) para el
   registro, o si hay que crearlo.
4. Confirmar las reglas de validación vigentes con el usuario si no
   están ya definidas en código:
   - Email único (contra el repositorio).
   - Password: longitud mínima — **confirmar el número exacto**, no
     asumir 8 por defecto sin preguntarlo.
5. Si falta cualquiera de estos puntos, preguntar antes de proponer
   código. No completar los huecos con supuestos "razonables".

## Flujo de trabajo

### Paso 1 — DTO de entrada
- Definir (o confirmar el existente) `RegistrarUsuarioDTO`/schema
  Pydantic con `email` y `password`.
- Validaciones de formato (ej. `EmailStr` de Pydantic) van acá, no en
  el caso de uso.

### Paso 2 — Caso de uso `RegistrarUsuarioUseCase`
- Recibe el DTO, el repositorio y el `IPasswordHasher` por inyección
  de dependencias (constructor), siguiendo el mismo patrón que ya usan
  otros casos de uso del proyecto — verificar ese patrón antes de
  escribir (no asumir que es idéntico a otro módulo sin haberlo leído).
- Flujo interno esperado:
  1. Verificar si ya existe un usuario con ese email (repositorio).
     Si existe, lanzar la excepción de dominio correspondiente (ver
     qué excepciones ya existen en el proyecto antes de crear una
     nueva del mismo tipo).
  2. Validar longitud mínima de password (según lo confirmado en
     precondiciones).
  3. Hashear el password (`await password_hasher.hash(...)`).
  4. Construir la entidad `Usuario` con los datos + hash.
  5. Persistir vía repositorio.
  6. Devolver el resultado (DTO de salida, sin el hash ni el password
     en texto plano).

### Paso 3 — Excepciones de dominio
- Antes de crear una excepción nueva (ej. `EmailYaRegistradoError`),
  revisar si el proyecto ya tiene una jerarquía de excepciones de
  dominio existente y seguir esa convención.

### Paso 4 — Endpoint FastAPI
- `POST /auth/register` — leer el router real y el estilo de manejo
  de errores HTTP ya usado en otros endpoints (para mapear la
  excepción de dominio al código HTTP correcto, normalmente 409 para
  email duplicado) antes de escribir el nuevo endpoint.

### Paso 5 — Verificación posterior
- Releer el caso de uso completo después de escribirlo.
- Confirmar con el usuario antes de pasar al login (`LoginUseCase`) o
  a cualquier otro caso de uso.

## Reglas anti-alucinación específicas de este skill

- Nunca inventar el nombre de un método del repositorio: si no se
  confirmó, preguntar "¿cómo se llama el método para buscar por
  email?" en vez de escribir uno plausible.
- Nunca asumir el largo mínimo de password sin que el usuario lo haya
  dicho explícitamente en esta conversación.
- Nunca devolver el hash de password ni el password en texto plano en
  la respuesta del endpoint — si el DTO de salida no está definido,
  proponerlo explícitamente y pedir confirmación.
- Si el usuario pide "segui" sin más detalle, avanzar un solo paso del
  flujo de arriba (no escribir DTO + caso de uso + endpoint de una).

## Formato de salida esperado en cada paso

1. Qué se leyó/confirmó antes de este paso.
2. Código propuesto.
3. Qué falta confirmar antes de continuar.