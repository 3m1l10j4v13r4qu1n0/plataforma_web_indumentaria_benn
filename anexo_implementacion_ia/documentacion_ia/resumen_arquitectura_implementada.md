---

# 🏛️ Resumen de la Arquitectura Implementada

## 1. Visión y Alcance
Se ha modernizado el núcleo del sistema retail, eliminando procesos manuales y garantizando la integridad de las operaciones de venta, consulta de stock, cambios y auditoría de inventario. El sistema prioriza la agilidad para el Vendedor y Cajero, la supervisión para el Gerente/Encargado, y la protección de las reglas de negocio transversales.

## 2. Patrón Arquitectónico: Clean + Hexagonal (Ports & Adapters)
El proyecto se estructura en capas concéntricas estrictamente desacopladas, donde las dependencias fluyen **siempre hacia el centro (Dominio)**.

*   **Dominio (`app/domain/`)**: El corazón del sistema. Contiene Entidades (`Venta`, `Producto`, `MovimientoStock`), Objetos de Valor (`Descuento`, `CondicionProducto`), Servicios Puros (`generar_numero_ticket`) y Puertos (`typing.Protocol`). **Cero dependencias externas** (sin FastAPI, sin SQLAlchemy, sin Pydantic).
*   **Aplicación (`app/application/`)**: Orquesta los casos de uso. Recibe los Puertos del dominio, coordina la lógica de flujo y lanza Excepciones de Dominio. No sabe cómo se persisten los datos ni cómo se presentan.
*   **Infraestructura (`app/infrastructure/`)**: Implementa los Puertos definidos en el dominio. Contiene los modelos ORM de SQLAlchemy, los Repositorios concretos y el contenedor de Inyección de Dependencias (`dependency_injection.py`).
*   **Presentación (`app/presentation/`)**: El borde exterior. Define los esquemas de validación de entrada/salida (Pydantic V2), los Routers (endpoints FastAPI) y el Manejo Centralizado de Excepciones (`handlers.py`).

## 3. Reglas Inquebrantables Aplicadas (SGVIR)
Durante todo el desarrollo, se respetaron rigurosamente las siguientes reglas:
1.  **Aislamiento del Dominio**: Ningún archivo en `app/domain/` importa librerías de terceros.
2.  **Inversión de Dependencias (DIP)**: Los Casos de Uso dependen de `IProductoRepository`, nunca de `ProductoRepository`.
3.  **Manejo Centralizado de Excepciones**: **Cero bloques `try/except`** en Routers o Casos de Uso para lógica de negocio. Todas las excepciones (`StockInsuficienteError`, `PlazoDeCambioVencidoError`, etc.) burbujean y son traducidas a respuestas HTTP estandarizadas (400, 403, 404, 409) exclusivamente en `handlers.py`.
4.  **Ciclo de Vida Transient**: Todos los repositorios y casos de uso se instancian por cada request HTTP, evitando estados compartidos y fugas de memoria en entornos concurrentes.

## 4. Decisiones de Diseño Destacadas (SOLID, KISS, DRY, YAGNI)
*   **SRP con Objetos de Valor**: La validación de descuentos (`Descuento`) y la condición de cambios (`CondicionProducto`) se encapsularon en Value Objects inmutables (`@dataclass(frozen=True)`), liberando a la entidad `Venta` de esa responsabilidad.
*   **Patrón Unit of Work (HU-08)**: Se introdujo `IUnitOfWork` para garantizar transacciones **ACID**. El descuento de stock y el registro del `MovimientoStock` ocurren en la misma transacción; si uno falla, se hace `rollback` de todo.
*   **KISS/YAGNI en Servicios Puros**: La generación del `numero_ticket` se implementó como una función pura de Python (`generar_numero_ticket`), evitando la sobre-ingeniería de crear una interfaz y un mock complejo para algo que no tiene estado ni dependencias externas.
*   **DRY en Repositorios**: Se centralizó la lógica de mapeo ORM → Dominio en métodos auxiliares (ej. `_map_to_domain`) para evitar duplicación de código.

## 5. Historias de Usuario Completadas (Backlog)
| HU | Descripción | Estado |
| :--- | :--- | :--- |
| **HU-01** | Validar y descontar stock antes de vender. | ✅ Completado |
| **HU-02** | Validar plazo de 15 días para cambios. | ✅ Completado |
| **HU-03** | Validar estado del producto (NUEVO_CON_ETIQUETA). | ✅ Completado |
| **HU-04** | Solicitar y validar ticket de compra existente. | ✅ Completado |
| **HU-05** | Control de descuentos con autorización de Gerente. | ✅ Completado |
| **HU-06** | Consulta flexible de stock por nombre o código. | ✅ Completado |
| **HU-07** | Generación automática y única del ticket de venta. | ✅ Completado |
| **HU-08** | Actualización atómica de stock con trazabilidad (MovimientoStock). | ✅ Completado |

## 6. Estrategia de Testing (TDD)
Cada caso de uso cuenta con pruebas unitarias de aislamiento en `tests/unit/`. Se utilizaron **Fakes en memoria** (`FakeProductoRepository`, `FakeUnitOfWork`, etc.) que implementan los mismos `Protocol` del dominio, garantizando que las pruebas sean rápidas, deterministas y no requieran una base de datos real.

---
