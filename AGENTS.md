# AGENTS.md — SGVIR (Plataforma Web Indumentaria Benn)

Monorepo académico: sistema de ventas e inventario retail. Backend **FastAPI** (Clean/Hexagonal Architecture) + frontend **React/Vite/TS**. Respondé en español latinoamericano.

## Fuentes de verdad

- **Historias de usuario**: `docs/04_historias_usuario/HU-XX/` son la fuente de verdad (Gherkin, criterios de aceptación, API, pruebas). NUNCA asumas su contenido de memoria: leelas antes de implementar.
- **Skills obligatorios** (flujo de trabajo, se activan por tarea):
  - Backend: `.opencode/skills/di-architect-scaffold/SKILL.md`
  - Frontend: `.opencode/skills/fe-architect-scaffold/SKILL.md`
  - Ambos usan un flujo de 6 pasos y esperan confirmación explícita ("Continuar") entre pasos.
- **Reglas del proyecto**: `.opencode/rules/*.md` (stack, reglas de negocio, calidad de arquitectura, roadmap).
- Los README.md están desactualizados en varios puntos (ESLint, `/health`, alembic init). Confiá en `package.json`, `requirements.txt` y el código real antes que en la prosa.

## Backend (`src/backend/`)

- Requiere **Python 3.14.6** (`.python-version`, pyenv). Comandos SIEMPRE desde `src/backend/`.
- Setup: `python -m venv venv && pip install -r requirements.txt && cp .env.example .env` (`DATABASE_URL` postgresql+asyncpg://... es obligatorio).
- Levantar: `uvicorn app.main:app --reload` (docs en `/api/docs`).
- **Health check es `GET /`** (devuelve `{"estado":"ok",...}`). NO existe `/health` aunque el frontend lo declare en `endpoints.ts`.
- Tests: `pytest` (usa `@pytest.mark.asyncio`, fakes en memoria de `tests/unit/fakes/`, no requiere DB). Los imports son `from app.*` y `from tests.unit.*`, por eso corren desde la raíz del backend.
- Lint/format: `ruff check .` y `black .` (antes de commitear).
- Migraciones: `alembic revision --autogenerate -m "..."` + `alembic upgrade head`. **Gotcha**: `alembic/env.py` NO importa los modelos ORM (línea comentada), así que autogenerate no detecta tablas nuevas hasta que los imports se agreguen ahí.
- Arquitectura estricta (no la rompas):
  - `app/domain/` = Python puro, sin FastAPI/SQLAlchemy/Pydantic. Define contratos con `typing.Protocol`.
  - `app/infrastructure/` implementa los ports (repositorios, ORM, `dependency_injection.py` con `Depends`).
  - `app/application/use_cases/` recibe SOLO ports en `__init__`, nunca implementaciones concretas.
  - Excepciones de dominio se mapean a HTTP SOLO en `app/presentation/handlers.py`. Prohibido `try/except` de negocio en routers/casos de uso.

## Frontend (`src/frontend/`)

- Stack real (los README dicen otro): React 19, Vite 8, TypeScript strict, React Router v7, Tailwind v4 (plugin `@tailwindcss/vite`, SIN `tailwind.config.js`/`postcss.config.js`).
- Scripts: `npm run dev` (puerto 5173), `npm run build` (`tsc -b && vite build`), `npm run test` (Vitest), `npm run preview`.
- **Lint = `npm run lint` usa `oxlint`**, no ESLint (config en `.oxlintrc.json`). No existe script `format`.
- Alias `@` → `./src`. Proxy de dev: `/api/*` → `http://localhost:8000`.
- Reglas duras (ver skill `fe-architect-scaffold`):
  - Prohibido `any`, prohibido inventar endpoints (solo los de `src/api/endpoints.ts`), prohibida lógica de negocio en componentes presentacionales.
  - Tipos en `src/types/api/` deben reflejar exactamente los esquemas Pydantic.
  - Errores HTTP centralizados (interceptor Axios / ErrorBoundary), sin `try/catch` dispersos.
  - NO implementar autenticación real (YAGNI; backend aún no la tiene).
- HU-06 (Consultar stock) es la única pantalla real hoy; el resto de la app aún es el starter de Vite.

## Convenciones de trabajo

- **Commits en español, estilo Conventional Commits** con scope en minúsculas: `feat(utils): se agrega funcion cn a utils`, `chore(backend): ...`, `docs: ...`. No en inglés, no mensajes vagos.
- **Ramas**: prohibido trabajar sobre `main`. Crear `feature/*` o `fix/*` a partir de `develop`.
- Cada HU sigue los 6 pasos del skill correspondiente; antes de tocar código, leé la doc de la HU.
- Toda funcionalidad nueva debe mantener actualizados: README, `.env.example`, y la tabla de endpoints en `fe-architect-scaffold/SKILL.md`.