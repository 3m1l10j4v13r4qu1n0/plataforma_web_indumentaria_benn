# Stack Tecnológico Obligatorio — SGVIR

Este proyecto DEBE respetar siempre el siguiente stack. No introducir alternativas sin confirmación explícita del usuario.

- **Lenguaje:** Python 3.14+
- **Framework Web:** FastAPI
- **Validación de datos:** Pydantic V2 (usar `BaseModel`, no dataclasses para DTOs)
- **ORM:** SQLAlchemy 2.0 con soporte asíncrono (`AsyncSession`, `async def`)
- **Migraciones:** Alembic
- **Base de datos:** PostgreSQL en producción. SQLite permitido únicamente para pruebas locales/tests.
- **Testing:** Pytest + pytest-asyncio
- **Estándares de código:**
  - Type hints estrictos en todo el código (funciones, métodos, atributos de clase).
  - Cumplir PEP 8.
  - Docstrings en formato Google style para funciones, clases y métodos públicos.
