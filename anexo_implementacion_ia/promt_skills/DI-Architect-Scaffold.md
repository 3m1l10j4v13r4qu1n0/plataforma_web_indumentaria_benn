# 🛠️ Skill: DI-Architect-Scaffold

## 🎯 Propósito
Estandarizar la implementación de la **Inyección de Dependencias (DI)** y el flujo de trabajo en proyectos basados en **Clean Architecture + Hexagonal Architecture (Ports & Adapters)**, garantizando bajo acoplamiento, alta cohesión y facilitando las pruebas unitarias.

## 📜 Reglas Inquebrantables del Proyecto (SGVIR)
1. **Aislamiento del Dominio**: La carpeta `app/domain/` NO puede importar nada de FastAPI, SQLAlchemy, Pydantic o librerías externas. Solo Python puro.
2. **Inversión de Dependencias (DIP)**: El dominio define los contratos (`typing.Protocol`). La infraestructura los implementa. Los casos de uso solo conocen los contratos, nunca las implementaciones concretas.
3. **Manejo Centralizado de Excepciones**: Prohibido usar bloques `try/except` para errores de negocio en los Routers o Casos de Uso. Todas las excepciones de dominio deben ser capturadas y traducidas a respuestas HTTP estandarizadas exclusivamente en `app/presentation/handlers.py`.
4. **Ciclo de Vida de Dependencias**: 
   - `Singleton`: Configuraciones, motores de BD.
   - `Transient` (por request): Repositorios y Casos de Uso (para evitar estados compartidos y fugas de memoria en concurrencia).
5. **Estructura de Carpetas Estricta**: Respetar la estructura definida en el `README.md` del proyecto.

---

## 🔄 Flujo de Trabajo Estándar (6 Pasos)

Cada vez que se solicite implementar una nueva Historia de Usuario (HU) o módulo, se debe seguir estrictamente este orden:

### Paso 1: Definición de Contratos y Excepciones (Dominio)
- **Ubicación**: `app/domain/`
- **Acciones**:
  1. Crear/Actualizar la Entidad de Dominio (`app/domain/models/`) con validación de invariantes en `__post_init__` o factory.
  2. Definir las Excepciones de Dominio específicas en `app/domain/exceptions.py` (heredando de una `DomainException` base).
  3. Definir el Puerto/Contrato en `app/domain/ports/` usando `typing.Protocol` (ej. `IProductRepository`).

### Paso 2: Implementación de Adaptadores Concretos (Infraestructura)
- **Ubicación**: `app/infrastructure/database/`
- **Acciones**:
  1. Crear el modelo ORM de SQLAlchemy en `orm_models/`.
  2. Crear la clase del repositorio en `repositories/` que implemente el `Protocol` definido en el Paso 1.
  3. El repositorio debe lanzar las **Excepciones de Dominio** (no excepciones de SQLAlchemy) cuando se violen reglas de negocio (ej. duplicados).

### Paso 3: Configuración del Wiring (Inyección de Dependencias)
- **Ubicación**: `app/infrastructure/dependencies/dependency_injection.py`
- **Acciones**:
  1. Crear funciones "getter" (fábricas) que devuelvan instancias de los Casos de Uso.
  2. Estas funciones deben instanciar el Repositorio Concreto e inyectarlo en el Caso de Uso.
  3. Usar `Depends` de FastAPI en estas funciones para gestionar el ciclo de vida por request (especialmente para la sesión de BD).

### Paso 4: Lógica de Negocio (Capa de Aplicación)
- **Ubicación**: `app/application/use_cases/`
- **Acciones**:
  1. Crear la clase del Caso de Uso (ej. `CreateProductUseCase`).
  2. El `__init__` debe recibir **únicamente** los Puertos (Interfaces), nunca implementaciones concretas.
  3. El método `execute` orquesta la lógica, llama al puerto y deja que las excepciones de dominio burbujeen hacia arriba.

### Paso 5: Exposición y Manejo de Errores (Capa de Presentación)
- **Ubicación**: `app/presentation/`
- **Acciones**:
  1. Definir DTOs de entrada/salida con Pydantic en `schemas/`.
  2. Definir el endpoint en `routers/`, inyectando el Caso de Uso mediante `Depends(getter_del_paso_3)`.
  3. **Regla Crítica**: En `handlers.py`, registrar `@app.exception_handler(TuExcepcionDeDominio)` para mapear cada error de negocio a su código HTTP correspondiente (400, 403, 404, 409, etc.) con un payload JSON estandarizado.

### Paso 6: Pruebas de Aislamiento (Testing)
- **Ubicación**: `tests/unit/`
- **Acciones**:
  1. Crear un `FakeRepository` en memoria que implemente el mismo `Protocol` del dominio.
  2. Inyectar este fake en el Caso de Uso.
  3. Escribir tests que verifiquen el comportamiento exitoso y que se lancen las excepciones de dominio correctas ante datos inválidos, sin tocar la BD real.

---

## 📋 Plantilla de Estructura de Archivos (Ejemplo Módulo "X")

```text
app/
├── domain/
│   ├── models/x.py                # Entidad pura + validaciones
│   ├── ports/ix_repository.py     # typing.Protocol
│   └── exceptions.py              # XAlreadyExistsError, InvalidXDataError
├── infrastructure/
│   ├── database/orm_models/x_orm.py       # SQLAlchemy Model
│   ├── database/repositories/x_repository.py # Implementa IXRepository
│   └── dependencies/dependency_injection.py  # get_x_use_case() con Depends
├── application/
│   └── use_cases/create_x_use_case.py     # Recibe IXRepository en __init__
└── presentation/
    ├── schemas/x_schema.py                # Pydantic Models
    ├── routers/x_router.py                # Endpoint POST /x con Depends
    └── handlers.py                        # @app.exception_handler(...)

    ```
---

# 🌱 Cultura de Desarrollo de Software (Developer Culture)

El objetivo es mantener un código limpio, mantenible y fácil de entender, fomentando hábitos de trabajo similares a los utilizados en equipos profesionales.

## 📌 Principios Fundamentales

### 1. Código Limpio (Clean Code)
- Los nombres de variables, clases y funciones deben ser descriptivos.
- Cada función debe tener una única responsabilidad.
- Evitar métodos excesivamente largos.
- Priorizar la legibilidad antes que la complejidad.

### 2. Principios SOLID
- **S (Single Responsibility):** cada clase debe tener una sola responsabilidad.
- **O (Open/Closed):** el código debe estar abierto a extensión y cerrado a modificación.
- **L (Liskov Substitution):** las implementaciones deben poder sustituir a sus abstracciones.
- **I (Interface Segregation):** interfaces pequeñas y específicas.
- **D (Dependency Inversion):** depender de abstracciones y no de implementaciones.

### 3. KISS (Keep It Simple)
- Implementar la solución más simple posible.
- Evitar complejidad innecesaria.

### 4. DRY (Don't Repeat Yourself)
- No duplicar lógica de negocio.
- Reutilizar componentes y abstraer código repetido.

### 5. YAGNI (You Aren't Gonna Need It)
- No implementar funcionalidades que todavía no son necesarias.

---

# 🌿 Estrategia de Ramas

Prohibido trabajar directamente sobre `main`.

Estructura recomendada:

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

## Convenciones

| Tipo de Rama | Ejemplo |
|---------------|---------|
| Nueva funcionalidad | `feature/create-product` |
| Corrección de errores | `fix/login-error` |
| Refactorización | `refactor/user-service` |
| Documentación | `docs/readme` |
| Pruebas | `test/product-use-case` |
| Configuración | `chore/dependencies` |

---

# 📝 Convención de Commits

Todos los commits deben seguir el estándar **Conventional Commits**.

## Formato

```text
<tipo>: <descripción breve>
```

Ejemplos:

```bash
git commit -m "feat: agregar endpoint para crear productos"
git commit -m "fix: corregir validación de email"
git commit -m "docs: actualizar README"
git commit -m "refactor: separar lógica de autenticación"
git commit -m "test: agregar pruebas del caso de uso de productos"
git commit -m "chore: actualizar dependencias"
```

## Tipos permitidos

| Prefijo | Propósito |
|-----------|----------|
| feat | Nueva funcionalidad |
| fix | Corrección de errores |
| docs | Documentación |
| refactor | Reorganización del código |
| test | Pruebas |
| style | Formato del código |
| chore | Configuración y mantenimiento |
| build | Dependencias y compilación |
| ci | Integración continua |
| perf | Optimización |
| revert | Revertir cambios |

---

# 🔄 Filosofía de Commits

### ✅ Commit Atómico
Cada commit debe representar un único cambio.

Correcto:

```text
feat: implementar CRUD de productos
```

Incorrecto:

```text
cambios varios
```

### ✅ Commits Pequeños y Frecuentes

Preferir:

- 10 commits pequeños

En lugar de:

- 1 commit gigante con muchos cambios mezclados.

---

# 🧪 Calidad del Código

Antes de realizar un commit o Pull Request verificar:

```bash
ruff check .
black .
pytest
```

No se debe subir código que:

- No compile.
- Rompa pruebas existentes.
- Contenga código comentado innecesario.
- Tenga imports sin usar.

---

# 📚 Documentación

Toda funcionalidad nueva debe actualizar:

- README.md
- Variables de entorno (`.env.example`)
- Diagramas si corresponde
- Endpoints y ejemplos de uso
- Casos de uso afectados

---

# 🔍 Revisión de Código

Antes de fusionar una rama:

- Revisar los cambios con:

```bash
git diff
git status
```

- Verificar que la rama esté actualizada respecto de `develop`.
- Resolver conflictos antes del merge.
- Mantener Pull Requests pequeños y fáciles de revisar.

---

# 🚫 Reglas Prohibidas

- Trabajar directamente sobre `main`.
- Hacer commits con mensajes como:

```text
cambios
arreglos
update
cosas
asd
```

- Duplicar lógica de negocio.
- Acoplar el dominio con FastAPI, SQLAlchemy o Pydantic.
- Ignorar excepciones mediante bloques `try/except` innecesarios.
- Crear clases o funciones excesivamente grandes.

---

# 🎯 Objetivo

Construir software mantenible, desacoplado y fácil de entender, aplicando los principios de Clean Architecture, Hexagonal Architecture, SOLID y las prácticas habituales utilizadas por equipos profesionales, adaptadas al contexto académico de estudiantes de segundo año de Analista de Sistemas.
