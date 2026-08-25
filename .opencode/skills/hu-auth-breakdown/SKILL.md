---
name: hu-auth-breakdown
description: >
  Implementa la capa de autenticación/login (dominio, casos de uso,
  infraestructura, interfaz y frontend) siguiendo Clean Architecture,
  con verificación obligatoria contra el código real antes de escribir
  o afirmar nada. Usar cuando el usuario pida agregar, modificar o
  revisar login, registro, tokens, sesiones, roles o permisos.
disable-model-invocation: true
---

# hu-auth-breakdown

## Propósito

Guiar la implementación de la capa de autenticación de
`plataforma_web_indumentaria_benn` en pasos controlados y verificables,
minimizando la posibilidad de que el agente invente nombres de archivos,
métodos, firmas de funciones o decisiones de arquitectura que no están
respaldadas por el código o por una decisión explícita del usuario.

Este skill NO asume que el agente conoce el proyecto de memoria.
Cada paso empieza por **leer el estado real** antes de proponer o
escribir código.

Autenticación (login/sesión) y autorización (roles/permisos) se tratan
como dos fases secuenciales y separadas — ver Paso 6a y 6b — con ramas
distintas (`feature/auth-autenticacion` y `feature/auth-autorizacion`).

## Regla de oro

> Si no lo leíste en este turno (código, HU, schema, config), no lo
> afirmes como si fuera un hecho. Decilo como propuesta o preguntá.

No usar frases como "ya que tu proyecto usa X" o "como definiste antes"
salvo que X se haya visto en el archivo leído en esta sesión de trabajo.

## Precondiciones (verificar antes de tocar código)

1. Leer la estructura de carpetas real del proyecto (`ls` / `tree` en
   los directorios de `domain`, `application`, `infrastructure`,
   `interface` o los nombres equivalentes que use el repo).
2. Leer al menos un caso de uso existente completo (ej. el de
   `ConsultarStockUseCase` o similar) para confirmar convenciones reales:
   naming, uso de `Protocol` vs `ABC`, manejo de errores, estilo de DTOs.
3. Leer el `CLAUDE.md` y reglas SOLID del repo si existen.
4. Si alguna convención no está clara o no aparece en el código leído,
   preguntar antes de asumir. No inventar un patrón "razonable"
   sin chequearlo.

## Flujo de trabajo (ejecutar en este orden, un paso por vez)

### Paso 1 — Inventario y confirmación de alcance
- Listar qué endpoints/HU existentes deberían quedar protegidos.
- Confirmar con el usuario: JWT vs sesiones, si hay roles, si hay
  refresh token, dónde vive el modelo `Usuario` (tabla nueva o
  existente).
- No avanzar al Paso 2 sin esta confirmación explícita.

### Paso 2 — Dominio
- Proponer la entidad `Usuario` y los puertos (`PasswordHasherPort`,
  `TokenServicePort`, `UsuarioRepositoryPort`) como código, citando en
  qué archivo se ubicarían según la estructura real leída en las
  precondiciones.
- Mostrar el código al usuario antes de escribir el archivo si el
  cambio afecta más de un módulo.

### Paso 3 — Casos de uso
- Un caso de uso a la vez (`RegistrarUsuarioUseCase`, `LoginUseCase`,
  `ObtenerUsuarioActualUseCase`).
- Cada caso de uso debe poder ejecutarse/testearse antes de pasar al
  siguiente. No generar los tres de una sola vez sin revisión intermedia.

### Paso 4 — Infraestructura
- Implementar los adaptadores concretos (`BcryptPasswordHasher`,
  `JWTTokenService`, repositorio SQLAlchemy de `Usuario`).
- Verificar contra `requirements.txt`/`pyproject.toml` reales qué
  librerías ya están instaladas antes de recomendar una nueva
  (ej. no asumir que `python-jose` está disponible sin comprobarlo).

### Paso 5 — Interfaz (FastAPI)
- Endpoints y dependencias (`get_current_user`, `require_role`).
- Verificar el router real y el patrón de inyección de dependencias
  usado en los endpoints existentes antes de escribir los nuevos.

### Paso 6a — Proteger HU existentes (autenticación)
- Rama sugerida: `feature/auth-autenticacion`.
- Ir HU por HU, agregando solo `Depends(get_current_user)` (exige
  sesión válida, todavía sin chequeo de rol).
- Mostrar el diff propuesto antes de aplicarlo. No modificar más de
  una HU por confirmación del usuario.
- Esta fase se puede mergear a `develop` de forma independiente:
  cierra el circuito de "solo usuarios logueados pueden usar la API".

### Paso 6b — Autorización por rol/permiso (fase separada)
- Rama sugerida: `feature/auth-autorizacion`, abierta después de
  mergear la de autenticación.
- Definir el puerto/caso de uso de autorización (ej. `RoleCheckerPort`
  o `AutorizarAccionUseCase`) leyendo primero cómo quedó modelado el
  rol en el `Usuario` del dominio (Paso 2), no asumirlo de nuevo.
- Agregar `require_role(...)` (o equivalente) HU por HU, mismo
  criterio de una confirmación por HU antes de aplicar el diff.
- No mezclar en el mismo commit/PR cambios de autenticación (Paso 6a)
  con cambios de autorización (Paso 6b).

### Paso 7 — Frontend
- `AuthContext`, `ProtectedRoute`, interceptor de refresh.
- Leer el `App.tsx`/router real antes de proponer dónde se insertan
  las rutas protegidas.
- Si hay autorización por rol, el chequeo de rol en el frontend
  (ocultar/deshabilitar UI) va después de que el Paso 6b esté
  confirmado en el backend — no antes, para no mostrar una UI que
  el backend todavía no respalda.

## Reglas anti-alucinación (aplican en todos los pasos)

- **Nunca inventar** nombres de archivos, clases, métodos o rutas que
  no se hayan visto en el código leído en esta sesión. Si hace falta
  un nombre nuevo, decir explícitamente "este archivo/clase no existe,
  lo voy a crear como X".
- **Nunca citar** una librería, versión o API sin haberla confirmado
  en `requirements.txt`, `pyproject.toml`, `package.json` o
  documentación oficial leída en esta sesión.
- Si una instrucción del usuario es ambigua respecto a una decisión de
  arquitectura (JWT vs sesión, dónde va el modelo, etc.), preguntar en
  vez de asumir silenciosamente.
- Después de escribir o modificar un archivo, releerlo antes de seguir
  con el siguiente paso — no asumir que el cambio anterior quedó como
  se pensó.
- Si el usuario pide "segui" o "dale" sin más contexto, avanzar solo un
  paso del flujo de arriba, no varios de una.
- Ante cualquier duda entre "asumir" y "preguntar": preguntar.

## Formato de salida esperado en cada paso

1. Qué se leyó/verificó antes de proponer el cambio (lista corta).
2. Propuesta de código o diff.
3. Qué queda pendiente de confirmar antes del próximo paso.