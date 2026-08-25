# Sistema de Gestión de Ventas e Inventario Retail (SGVIR)

🛒 API REST para gestión de ventas e inventario  
📦 Control de stock en tiempo real  
🔄 Gestión de cambios y devoluciones  
🏗️ Clean Architecture + Hexagonal Architecture  
⚡ FastAPI  
🐍 Python  
🐘 PostgreSQL


---

## 📋 Tabla de Contenidos

- [Descripción general](#-descripción-general)
- [Objetivos del proyecto](#-objetivos-del-proyecto)
- [Documentación funcional](#-documentación-funcional)
- [Funcionalidades principales](#-funcionalidades-principales)
- [Alcance del Sistema](#-alcance-del-sistema)
- [Arquitectura](#-arquitectura)
- [Instalación y configuración](#-instalación-y-configuración)
- [Estructura del Proyecto — API REST](#️-estructura-del-proyecto--api-rest)
- [Resumen de Arquitectura](#-resumen-de-arquitectura)
- [Principios Aplicados](#-principios-aplicados)
- [Beneficios](#-beneficios)
- [Roadmap](#️-roadmap)
- [Tags](#-tags)




---

## 📌 Descripción general

El Sistema de Gestión de Ventas e Inventario Retail (SGVIR) es una API REST desarrollada para automatizar y centralizar la gestión de ventas, inventario y procesos de postventa dentro de un entorno comercial minorista.

La aplicación permite administrar productos, controlar el stock en tiempo real, registrar ventas, aplicar descuentos según permisos de usuario y gestionar cambios o devoluciones de productos mediante reglas de negocio definidas por la organización.

El sistema busca resolver problemas frecuentes en la operación comercial, como ventas sin stock disponible, aplicación de descuentos no autorizados y aceptación de devoluciones fuera de plazo o de productos en condiciones no permitidas.

Este proyecto fue desarrollado como ejercicio práctico de **análisis funcional y desarrollo backend**, aplicando principios de arquitectura limpia, diseño orientado al dominio y buenas prácticas de ingeniería de software.

**El alcance del proyecto se limita a la gestión de ventas, inventario y postventa, sin contemplar comercio electrónico, integración con pasarelas de pago ni gestión de proveedores.**

---

## 🎯 Objetivos del proyecto

### Objetivo General

Desarrollar una API REST que permita gestionar de forma segura y eficiente las operaciones de venta e inventario, garantizando la integridad de los datos y el cumplimiento de las políticas comerciales de la empresa.

### Objetivos Específicos

- Validar automáticamente la disponibilidad de stock antes de confirmar una venta.
- Actualizar el inventario de forma automática después de cada venta, cambio o devolución.
- Implementar controles para cambios y devoluciones mediante validación de ticket, plazo máximo permitido y estado del producto.
- Gestionar descuentos respetando los límites definidos para cada rol de usuario.
- Implementar flujos de autorización jerárquica para descuentos especiales.
- Mantener la trazabilidad de las operaciones realizadas dentro del sistema.
- Exponer la funcionalidad mediante una API REST preparada para futuras integraciones.

---

## 📚 Documentación funcional

La documentación del análisis funcional se encuentra en la carpeta `docs/`.

Incluye:

- Documento de visión
- Alcance del sistema
- Actores
- Requerimientos funcionales
- Reglas de negocio
- Casos de uso
- Diagramas de procesos
- Modelo conceptual de datos
- Historias de usuario
- Casos de prueba
- Especificación de API

Esta documentación simula los artefactos generados por un **Analista de Sistemas Junior** durante las etapas de relevamiento, análisis y diseño funcional.

---

## 🚀 Funcionalidades principales

### Gestión de Inventario

- Alta de productos.
- Consulta de productos.
- Modificación de productos.
- Baja lógica de productos.
- Consulta de stock en tiempo real.
- Actualización automática del stock.

### Gestión de Ventas

- Registro de ventas.
- Validación de disponibilidad de stock.
- Generación de ticket de venta.
- Descuento automático de inventario luego de cada venta.

### Gestión de Descuentos

- Aplicación de descuentos comerciales.
- Validación de porcentaje máximo permitido según rol.
- Solicitud de autorización para descuentos especiales.
- Registro de aprobaciones y rechazos.

### Gestión de Cambios y Devoluciones

- Validación obligatoria de ticket.
- Verificación de plazo máximo de 15 días.
- Control del estado físico del producto.
- Registro de cambios.
- Registro de devoluciones.
- Reintegro automático de stock cuando corresponde.

### Seguridad y Control

- Gestión de usuarios.
- Gestión de roles y permisos.
- Validación de reglas de negocio.
- Trazabilidad de operaciones.

---

## 🌐 API REST — Endpoints

Todos los endpoints de negocio viven bajo el prefijo `/api/v1`. La documentación interactiva (Swagger) está en `/api/docs`.

| Método | Ruta | Descripción | HU |
|--------|------|-------------|----|
| GET | `/` | Health check (`{"estado": "ok"}`) — **no existe `/health`** | — |
| GET | `/api/v1/productos/{codigo}/stock` | Consultar stock en tiempo real | HU-06 |
| GET | `/api/v1/productos/buscar?query=` | Buscar productos por código o nombre | HU-06 |
| POST | `/api/v1/ventas` | Validar stock, confirmar venta y generar ticket | HU-01 / HU-07 |
| GET | `/api/v1/ventas/validar-ticket/{numero_ticket}` | Validar existencia de ticket de compra | HU-04 |
| PATCH | `/api/v1/ventas/{numero_ticket}/estado` | Retener ticket en proceso de cambio | HU-04 |
| POST | `/api/v1/cambios` | Registrar cambio validando plazo de 15 días | HU-02 |
| POST | `/api/v1/cambios/{cambio_id}/validar-estado` | Registrar inspección física del producto | HU-03 |
| POST | `/api/v1/descuentos` | Aplicar descuento con autorización de gerente si excede el límite | HU-05 |

Códigos HTTP de errores de negocio (mapeados centralizadamente en `handlers.py`):

- `404` → recurso inexistente (producto, venta, cambio, ticket).
- `409` → conflictos (stock insuficiente, ticket duplicado, venta ya en cambio, falla de actualización de stock).
- `403` → plazo de cambio vencido.
- `422` → validaciones de negocio (descuento fuera de límite/sin autorización, producto no apto, observaciones requeridas).

---

## 🎯 Alcance del Sistema

### Funcionalidades contempladas (In-Scope)

- Gestión de productos.
- Gestión de inventario.
- Consulta de stock en tiempo real.
- Registro de ventas.
- Generación de tickets.
- Aplicación de descuentos.
- Gestión de cambios y devoluciones.
- Control de autorizaciones.
- Administración de usuarios y roles.

### Funcionalidades fuera del alcance (Out-of-Scope)

- Comercio electrónico (e-commerce).
- Ventas online.
- Integración con pasarelas de pago.
- Facturación electrónica.
- Gestión de proveedores.
- Gestión de compras.
- Integraciones con sistemas ERP externos.

---

## 🎯 Arquitectura

El proyecto sigue principios de **Clean Architecture**, separando:

- Capa de dominio
- Capa de aplicación
- Capa de infraestructura
- Capa de API

Esto permite mantener el sistema modular y mantenible.

---

## Tecnologías utilizadas

- Python 3.14
- FastAPI
- SQLAlchemy 2.0 (async) + Alembic
- PostgreSQL
- Pydantic V2
- Pytest + pytest-asyncio

---

## 🚀 Instalación y configuración

### Requisitos

- Python 3.14.6
- Git
- pyenv (recomendado)

Este proyecto incluye un archivo `.python-version` que indica la versión de Python utilizada durante el desarrollo.

Si utilizás **pyenv**, la versión correcta se seleccionará automáticamente al ingresar al directorio del proyecto.

```bash
pyenv install 3.14.6   # Solo si aún no la tenés instalada
pyenv local 3.14.6
```

Verificá la versión con:

```bash
python --version
```
---

```
# Clonar el repo

git clone git@github.com:3m1l10j4v13r4qu1n0/plataforma_web_indumentaria_benn.git


# posicionarse en la carpeta Backend
cd ./src/backend/


# Crear entorno virtual
python -m venv venv

# Linux 
source venv/bin/activate 

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Correr migraciones
# (Alembic ya viene inicializado en el repo — NO ejecutar `alembic init`)

# 1. aplica las migraciones existentes en PostgreSQL
alembic upgrade head

# 2. para generar una migración nueva tras cambiar modelos:
alembic revision --autogenerate -m "descripcion del cambio"
alembic upgrade head
```

> ⚠️ **Gotcha**: `alembic/env.py` no importa los modelos ORM automáticamente. Si creás tablas nuevas, agregá los imports de los modelos en ese archivo para que `--autogenerate` las detecte.

# Levantar la API
uvicorn app.main:app --reload

# Documentación interactiva
# http://localhost:8000/api/docs
```
---

# 🏗️ Estructura del Proyecto — API REST 

Este proyecto implementa una arquitectura basada en **Clean Architecture + Hexagonal (Ports & Adapters)**, separando claramente responsabilidades entre capas.

---

## 📦 Estructura General

```
backend/
│
├── alembic/
│   ├── versions/               💬 migraciones versionadas del esquema
│   ├── env.py                  💬 configuración de migraciones (importar modelos ORM aquí)
│   └── script.py.mako
│
├── app/
│   ├── main.py                 💬 punto de entrada FastAPI (health check en GET /)
│   │
│   ├── presentation/           🟦 capa de presentación (delivery)
│   │   ├── routers/
│   │   │   ├── producto_router.py    (stock, búsqueda — HU-06)
│   │   │   ├── venta_router.py       (ventas, ticket, validar-ticket — HU-01/04/07)
│   │   │   ├── cambio_router.py      (cambios e inspección — HU-02/03)
│   │   │   └── descuento_router.py   (descuentos — HU-05)
│   │   ├── schemas/
│   │   │   ├── producto_schema.py
│   │   │   ├── venta_schema.py
│   │   │   ├── cambio_schema.py
│   │   │   └── descuento_schema.py   💬 DTOs de entrada/salida (Pydantic V2)
│   │   └── handlers.py         💬 mapeo centralizado dominio → HTTP (único lugar con try/except)
│   │
│   ├── application/            🟩 capa de aplicación (use cases)
│   │   ├── dtos/
│   │   │   ├── venta_dto.py
│   │   │   ├── cambio_dto.py
│   │   │   └── descuento_dto.py
│   │   └── use_cases/
│   │       ├── validar_stock_venta_use_case.py        (HU-01/07: venta + ticket + descuento de stock)
│   │       ├── consultar_stock_producto_use_case.py   (HU-06)
│   │       ├── buscar_productos_use_case.py           (HU-06)
│   │       ├── validar_ticket_compra_use_case.py      (HU-04)
│   │       ├── marcar_venta_en_cambio_use_case.py     (HU-04)
│   │       ├── procesar_cambio_use_case.py            (HU-02)
│   │       ├── validar_estado_producto_use_case.py    (HU-03)
│   │       ├── actualizar_stock_use_case.py           (HU-08, atómico con UoW)
│   │       └── aplicar_descuento_use_case.py          (HU-05)
│   │
│   ├── domain/                 🟥 capa de dominio (core, Python puro sin frameworks)
│   │   ├── models/
│   │   │   ├── producto.py
│   │   │   ├── venta.py
│   │   │   ├── detalle_venta.py
│   │   │   ├── cambio.py
│   │   │   ├── descuento.py
│   │   │   └── movimiento_stock.py
│   │   ├── ports/              💬 contratos (typing.Protocol) → Ports & Adapters
│   │   │   ├── i_producto_repository.py
│   │   │   ├── i_venta_repository.py
│   │   │   ├── i_cambio_repository.py
│   │   │   ├── i_descuento_repository.py
│   │   │   ├── i_movimiento_stock_repository.py
│   │   │   ├── i_generador_numero_ticket.py
│   │   │   └── i_unit_of_work.py
│   │   └── exceptions.py       💬 excepciones de dominio (mapeadas solo en handlers.py)
│   │
│   └── infrastructure/         🟨 capa de infraestructura (adapters)
│       ├── core/
│       │   └── config.py       💬 settings (.env, DATABASE_URL)
│       ├── database/
│       │   ├── session.py              💬 AsyncSession / engine
│       │   ├── generador_numero_ticket.py  💬 generación única de tickets (HU-07)
│       │   ├── unit_of_work.py             💬 transacciones atómicas entre agregados (HU-08)
│       │   ├── orm_models/             💬 6 modelos SQLAlchemy (producto, venta, detalle,
│       │   │                              cambio, descuento, movimiento_stock)
│       │   └── repositories/           💬 implementaciones de los ports (5 repositorios)
│       └── dependencies/
│           └── dependency_injection.py 💬 fábricas con Depends (wiring por request)
│
├── tests/unit/                 💬 tests de aislamiento: fakes en memoria, sin DB real
│   ├── fakes/                      (7 fakes: repos + generador de ticket + UoW)
│   └── use_cases/                  (8 suites de casos de uso)
│
├── requirements.txt
├── alembic.ini
└── README.md
```

---

## 🧠 Resumen de Arquitectura

```
Presentation (FastAPI)
        ↓
Application (Use Cases)
        ↓
Domain (Entities + Rules + Ports)
        ↓
Infrastructure (DB, APIs externas)
```

---

## 🎯 Principios Aplicados

* ✔️ Separación de responsabilidades
* ✔️ Inversión de dependencias (DIP)
* ✔️ Arquitectura Hexagonal (Ports & Adapters)
* ✔️ Dominio desacoplado de frameworks
* ✔️ Código testeable y mantenible

---

## 🚀 Beneficios

* Escalable
* Testeable
* Independiente de tecnologías externas
* Fácil de mantener y extender

---

## 🗺️ Roadmap

- Fase 1: Análisis funcional ✔
- Fase 2: Diseño técnico y arquitectura ✔
- Fase 3: Implementación del módulo de productos ✔ (HU-06)
- Fase 4: Implementación del módulo de inventario ✔ (HU-08)
- Fase 5: Implementación del módulo de ventas ✔ (HU-01 / HU-07)
- Fase 6: Implementación del módulo de descuentos ✔ (HU-05)
- Fase 7: Implementación del módulo de cambios y devoluciones ✔ (HU-02 / HU-03 / HU-04)
- Fase 8: Pruebas unitarias ✔ (55 tests, fakes en memoria) — integración pendiente
- Fase 9: Documentación técnica 🚧 (en mejora continua)
---

## 🔖 Tags

- `hu-01-validar-stock-antes-de-vender` 👍
- `hu-02-validar-plazo-cambios`         
- `hu-03-validar-estado-producto-cambio`
- `hu-04-consultar-ticket-compra`
- `hu-05-controlar-descuentos`
- `hu-06-consulta-stock-disponible`
- `hu-07-generacion-ticket-venta`
- `hu-08-actualizacion-automatica-stock`  






## 🧠 Perfil objetivo

Este proyecto está pensado como material demostrativo para:

---

## Participantes

Emilio Javier Aquino   


## 📄 Licencia

Proyecto de uso educativo y demostrativo.
