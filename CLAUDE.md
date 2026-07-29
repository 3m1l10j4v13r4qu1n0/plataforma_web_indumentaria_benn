# Instrucciones generales

- Respondé SIEMPRE en español latinoamericano, tono informal (usá "vos", no "tú").
- Nunca respondas en inglés, incluso si el código, los logs, los mensajes de error o los comentarios están en inglés. Podés dejar nombres de variables, funciones, comandos y términos técnicos en inglés cuando corresponda (eso es normal), pero toda explicación tiene que estar en español.
- Sé directo y técnico. No hace falta que expliques cosas básicas de Python salvo que se pida.

# Sobre este proyecto

`plataforma_web_indumentaria_benn` es una plataforma web para una tienda de indumentaria (Sistema de Gestión de Ventas e Inventario Retail - SGVIR), compuesta por:

- **Backend:** FastAPI + SQLAlchemy (async), siguiendo Clean Architecture / arquitectura hexagonal / DDD. Detalle completo del flujo de scaffolding en la skill `di-architect-scaffold`.
- **Frontend:** React + Vite + TypeScript, con estructura alineada a las capas del backend. Detalle completo del flujo de scaffolding en la skill `fe-architect-scaffold`.

## Convenciones de arquitectura (backend)

- Separación estricta de capas: dominio (entidades, value objects, reglas de negocio) → casos de uso (application) → infraestructura (repositorios, ORM, adaptadores) → interfaz (routers FastAPI).
- Los puertos (interfaces) van segregados por responsabilidad (ISP), no un repositorio monolítico.
- La lógica de negocio y las validaciones de dominio no van en los routers ni en los modelos de SQLAlchemy; van en el dominio o en los casos de uso.
- Los schemas de Pydantic para entrada/salida son distintos de las entidades de dominio.
- Evitar imports circulares entre módulos del ORM; si aparece uno, avisar y proponer cómo romperlo (interfaces, imports diferidos, reestructuración de módulos).
- El detalle completo de reglas de negocio del SGVIR (stock, descuentos, cambios, tickets) vive en `di-architect-scaffold/SKILL.md`, no acá.

## Convenciones de arquitectura (frontend)

- Estructura de carpetas definida en `fe-architect-scaffold/SKILL.md`.
- Manejo de roles simulados (Vendedor, Cajero, Gerente) vía React Context + `useContext`. La autenticación real todavía no está implementada (se difiere a una fase posterior) — no asumas que hay login real salvo que se indique lo contrario.
- Los hooks custom van en su propio archivo; si detectás lógica duplicada entre hooks (como pasó con `useCrearVenta`), avisar antes de duplicar más código.

## Testing

- Si se agregan casos de uso o lógica de dominio nueva, proponer o escribir tests con pytest (backend) o Vitest + React Testing Library (frontend).
- No asumir que algo funciona sin correr los tests si están disponibles.

## Git / commits

- Nunca hagas commit sin que yo lo pida explícitamente en ese momento (además del permiso que ya pide Claude Code por `settings.json`).
- Convención de mensajes: español, formato corto y descriptivo con prefijo de tipo, ej: `fix: corrige mismatch async/sync en Alembic`, `feat: agrega endpoint de consulta de stock`. Prefijos permitidos: `feat`, `fix`, `docs`, `refactor`, `test`, `style`, `chore`, `build`, `ci`, `perf`, `revert`. Esta es la única convención de commits del proyecto — si alguna skill sugiere Conventional Commits en inglés, priorizá esta regla.
- Commits atómicos: un cambio lógico por commit, nunca "cambios varios".
- Prohibido trabajar directamente sobre `main`. Ramas: `feature/`, `fix/`, `refactor/`, `docs/`, `test/`, `chore/`.
- Nunca hagas `git push` sin que se pida explícitamente.

# Qué NO hacer sin preguntar

- No crear archivos nuevos sin avisar primero qué archivo y para qué (esto además está reforzado por `settings.json`, pero repetilo en tu razonamiento).
- No instalar dependencias nuevas (pip/npm) sin decir cuál y por qué antes de correr el comando.
- No modificar `alembic.ini`, `.env`, ni archivos de configuración de infraestructura sin avisar explícitamente qué se va a cambiar.
- No activar `di-architect-scaffold` o `fe-architect-scaffold` por tu cuenta sin que yo las invoque con `/di-architect-scaffold` o `/fe-architect-scaffold` explícitamente.