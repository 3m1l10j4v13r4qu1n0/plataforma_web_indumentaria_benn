---
name: di-architect-scaffold
description: Estandarizar la implementación de la Inyección de Dependencias (DI) y el flujo de trabajo en proyectos basados en Clean Architecture + Hexagonal Architecture (Ports & Adapters), garantizando bajo acoplamiento, alta cohesión y facilitando las pruebas unitarias. Usar cuando el usuario pida implementar una Historia de Usuario nueva, un caso de uso, repositorio, puerto, adapter, o endpoint en el backend del SGVIR.
disable-model-invocation: true
---

# DI Architect Scaffold

Skill para scaffoldear módulos del backend del **Sistema de Gestión de Ventas e Inventario Retail (SGVIR)**, siguiendo estrictamente Clean Architecture + Hexagonal Architecture.

## Stack tecnológico obligatorio

- Lenguaje: Python 3.14+
- Framework Web: FastAPI
- Validación de datos: Pydantic V2
- ORM: SQLAlchemy 2.0 (con soporte asíncrono vía `AsyncSession`)
- Migraciones: Alembic
- Base de datos: PostgreSQL (SQLite solo para pruebas locales)
- Testing: Pytest + pytest-asyncio
- Estándares de código: Type hints estrictos, PEP 8, docstrings en Google style

## 📜 Reglas Inquebrantables del Proyecto (SGVIR)

1. **Aislamiento del Dominio**: la carpeta `app/domain/` NO puede importar nada de FastAPI, SQLAlchemy, Pydantic o librerías externas. Solo Python puro.
2. **Inversión de Dependencias (DIP)**: el dominio define los contratos (`typing.Protocol`). La infraestructura los implementa. Los casos de uso solo conocen los contratos, nunca las implementaciones concretas.
3. **Manejo Centralizado de Excepciones**: prohibido usar bloques `try/except` para errores de negocio en Routers o Casos de Uso. Todas las excepciones de dominio deben capturarse y traducirse a respuestas HTTP estandarizadas exclusivamente en `app/presentation/handlers.py`.
4. **Ciclo de Vida de Dependencias**:
   - `Singleton`: configuraciones, motores de BD.
   - `Transient` (por request): repositorios y casos de uso (evita estados compartidos y fugas de memoria en concurrencia).
5. **Estructura de Carpetas Estricta**: respetar la estructura definida en el `README.md` del proyecto.

## 📌 Reglas de negocio críticas (NO ignorar)

1. **Stock**: el `stock_actual` de un producto NUNCA puede ser negativo. Ventas y devoluciones deben ser transacciones atómicas (ACID).
2. **Cambios** (HU-02, HU-03, HU-04): solo se permiten si: a) existe el ticket original, b) han pasado ≤ 15 días desde la compra, c) el producto está "NUEVO" y "CON ETIQUETA".
3. **Descuentos** (HU-05): límite máximo (ej. 20%). Si se supera, el sistema debe exigir y registrar el `gerente_id` que autorizó la operación.
4. **Tickets** (HU-07): el `numero_ticket` debe ser único y generado automáticamente al confirmar la venta.

## 📂 Historias de Usuario — fuente de verdad

Este skill opera sobre una HU puntual, indicada por el usuario al invocarlo (ej. "corré di-architect-scaffold sobre HU-06" o pasando la ruta directa `docs/04_historias_usuario/HU-06/HU-06-Consultar_stock_disponible.md`).

**Nunca asumas el contenido de una HU de memoria ni te bases en resúmenes previos.** El listado de reglas de negocio críticas de arriba es contexto general del dominio, no reemplaza la HU real. Antes de tocar código, siempre leé con la herramienta Read el archivo Markdown de la HU indicada en `docs/04_historias_usuario/HU-XX/`, y extraé de ahí: descripción, criterios de aceptación, reglas de validación específicas y casos borde.

Si el usuario no especifica qué HU, preguntá cuál antes de avanzar — no lo asumas.

## 🔄 Flujo de trabajo estándar (6 pasos)

Cada vez que se solicite implementar una nueva Historia de Usuario (HU) o módulo, seguir estrictamente este orden y **esperar confirmación explícita ("Continuar") antes de avanzar al siguiente paso**.

### Paso 1: Definición de Contratos y Excepciones (Dominio)
**Ubicación**: `app/domain/`

**Antes de empezar**, leer con la herramienta Read el archivo de la HU indicada (`docs/04_historias_usuario/HU-XX/HU-XX_*.md`), enfocándote en: entidades involucradas, invariantes de negocio y reglas de validación. Si existen entidades de dominio relacionadas ya implementadas (ej. `app/domain/models/producto.py`), leerlas también para mantener consistencia de estilo y convenciones de nombres.

1. Crear/actualizar la Entidad de Dominio (`app/domain/models/`) con validación de invariantes en `__post_init__` o factory.
2. Definir las Excepciones de Dominio específicas en `app/domain/exceptions.py` (heredando de una `DomainException` base).
3. Definir el Puerto/Contrato en `app/domain/ports/` usando `typing.Protocol` (ej. `IProductRepository`).

### Paso 2: Implementación de Adaptadores Concretos (Infraestructura)
**Ubicación**: `app/infrastructure/database/`

**Antes de empezar**, leer un repositorio ya implementado similar (ej. `app/infrastructure/database/repositories/producto_repository.py`) para replicar el patrón de mapeo ORM ↔ Entidad de dominio, y evitar los bugs de mapeo ya corregidos anteriormente en el proyecto.

1. Crear el modelo ORM de SQLAlchemy en `orm_models/`.
2. Crear la clase del repositorio en `repositories/` que implemente el `Protocol` del Paso 1.
3. El repositorio debe lanzar **Excepciones de Dominio** (no excepciones de SQLAlchemy) cuando se violen reglas de negocio (ej. duplicados).

### Paso 3: Configuración del Wiring (Inyección de Dependencias)
**Ubicación**: `app/infrastructure/dependencies/dependency_injection.py`

**Antes de empezar**, leer el archivo `dependency_injection.py` completo tal como está para no duplicar getters ya existentes ni romper el estilo de las fábricas actuales.

1. Crear funciones "getter" (fábricas) que devuelvan instancias de los Casos de Uso.
2. Estas funciones deben instanciar el Repositorio Concreto e inyectarlo en el Caso de Uso.
3. Usar `Depends` de FastAPI en estas funciones para gestionar el ciclo de vida por request (especialmente para la sesión de BD).

### Paso 4: Lógica de Negocio (Capa de Aplicación)
**Ubicación**: `app/application/use_cases/`

**Antes de empezar**, releer los criterios de aceptación de la HU (ya leída en el Paso 1) — esta capa es donde esos criterios se traducen en lógica ejecutable. Si hay un caso de uso similar ya implementado (ej. `ConsultarStockUseCase`), leerlo como referencia de estructura.

1. Crear la clase del Caso de Uso (ej. `CreateProductUseCase`).
2. El `__init__` debe recibir **únicamente** los Puertos (Interfaces), nunca implementaciones concretas.
3. El método `execute` orquesta la lógica, llama al puerto y deja que las excepciones de dominio burbujeen hacia arriba.
4. **Regla crítica**: si el endpoint necesita datos de varias entidades para su respuesta (ej. nombres de productos en una venta), el caso de uso debe resolverlos y devolver un **DTO de aplicación** (en `app/application/dtos/`) listo para presentar. El router NUNCA accede a repositorios ni a puertos de persistencia (estándar establecido en `fix/hu-01-router-arquitectura`; ver `venta_router.py` como referencia).

### Paso 5: Exposición y Manejo de Errores (Capa de Presentación)
**Ubicación**: `app/presentation/`

**Antes de empezar**, leer `app/presentation/handlers.py` para ver qué excepciones ya están mapeadas y no duplicar handlers, y leer la tabla de endpoints en `fe-architect-scaffold/SKILL.md` para mantenerla sincronizada.

1. Definir DTOs de entrada/salida con Pydantic en `schemas/`.
2. Definir el endpoint en `routers/`, inyectando el Caso de Uso mediante `Depends(getter_del_paso_3)`. Los routers solo importan casos de uso y schemas propios: prohibido inyectar repositorios o puertos directamente.
3. **Regla crítica**: en `handlers.py`, registrar `@app.exception_handler(TuExcepcionDeDominio)` para mapear cada error de negocio a su código HTTP correspondiente (400, 403, 404, 409, etc.) con payload JSON estandarizado.

### Paso 6: Pruebas de Aislamiento (Testing)
**Ubicación**: `tests/unit/`

**Antes de empezar**, releer los criterios de aceptación de la HU (Paso 1) para asegurar que cada uno tenga al menos un test correspondiente.

1. Crear un `FakeRepository` en memoria que implemente el mismo `Protocol` del dominio.
2. Inyectar este fake en el Caso de Uso.
3. Escribir tests que verifiquen el comportamiento exitoso y que se lancen las excepciones de dominio correctas ante datos inválidos, sin tocar la BD real.

## 📋 Plantilla de estructura de archivos (ejemplo módulo "X")

```text
app/
├── domain/
│   ├── models/x.py                    # Entidad pura + validaciones
│   ├── ports/ix_repository.py         # typing.Protocol
│   └── exceptions.py                  # XAlreadyExistsError, InvalidXDataError
├── infrastructure/
│   ├── database/orm_models/x_orm.py           # SQLAlchemy Model
│   ├── database/repositories/x_repository.py  # Implementa IXRepository
│   └── dependencies/dependency_injection.py   # get_x_use_case() con Depends
├── application/
│   └── use_cases/create_x_use_case.py # Recibe IXRepository en __init__
└── presentation/
    ├── schemas/x_schema.py            # Pydantic Models
    ├── routers/x_router.py            # Endpoint POST /x con Depends
    └── handlers.py                    # @app.exception_handler(...)
```

## 🌱 Cultura de Desarrollo de Software

Mantener código limpio, mantenible y fácil de entender, con hábitos de trabajo profesionales.

### Principios
- **Clean Code**: nombres descriptivos, una responsabilidad por función, evitar métodos largos, priorizar legibilidad.
- **SOLID**: SRP, Open/Closed, Liskov, Interface Segregation, Dependency Inversion.
- **KISS**: la solución más simple posible.
- **DRY**: no duplicar lógica de negocio.
- **YAGNI**: no implementar funcionalidades que todavía no son necesarias.

### Estrategia de ramas

Prohibido trabajar directamente sobre `main`.

```text
main
│
└── develop
    ├── feature/product
    ├── feature/category
    ├── fix/login-validation
    ├── refactor/product-service
    ├── docs/readme
    └── test/product-use-case
```

### Convención de commits

**Usar la convención definida en `CLAUDE.md` del proyecto** (español, prefijo + descripción breve, ej. `feat: agregar endpoint para crear productos`). No usar Conventional Commits en inglés salvo indicación explícita.

### Calidad del código

Antes de commitear o abrir un PR, verificar:
```bash
ruff check .
black .
pytest
```

No subir código que: no compile, rompa tests existentes, tenga código comentado innecesario, o tenga imports sin usar.

### Documentación

Toda funcionalidad nueva debe actualizar: `README.md`, `.env.example`, diagramas si corresponde, y la tabla de endpoints en `fe-architect-scaffold/SKILL.md` si agrega un endpoint nuevo consumible por el frontend.

### Revisión de código

Antes de fusionar una rama: revisar con `git diff` / `git status`, verificar que esté actualizada respecto de `develop`, resolver conflictos antes del merge, mantener PRs pequeños.

### Prohibido

- Trabajar sobre `main`.
- Commits con mensajes vagos ("cambios", "arreglos", "update").
- Duplicar lógica de negocio.
- Acoplar el dominio con FastAPI, SQLAlchemy o Pydantic.
- Ignorar excepciones con `try/except` innecesarios.
- Clases o funciones excesivamente grandes.

## 🎯 Objetivo

Construir software mantenible, desacoplado y fácil de entender, aplicando Clean Architecture, Hexagonal Architecture, SOLID y prácticas de equipos profesionales.