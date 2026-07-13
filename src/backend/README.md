# Sistema de Gestión de Ventas e Inventario Retail (SGVIR)

🛒 API REST para gestión de ventas e inventario  
📦 Control de stock en tiempo real  
🔄 Gestión de cambios y devoluciones  
🏗️ Clean Architecture + Hexagonal Architecture  
⚡ FastAPI  
🐍 Python  
🐘 PostgreSQL

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
- Integraciones con sistemas ERP externos.---

## Arquitectura

El proyecto sigue principios de **Clean Architecture**, separando:

- Capa de dominio
- Capa de aplicación
- Capa de infraestructura
- Capa de API

Esto permite mantener el sistema modular y mantenible.

---

## Tecnologías utilizadas

- Python
- FastAPI
- PostgreSQL
- Pydantic

---

## 🚀 Instalación y configuración

### Requisitos

- Python 3.11.5
- Git
- pyenv (recomendado)

Este proyecto incluye un archivo `.python-version` que indica la versión de Python utilizada durante el desarrollo.

Si utilizás **pyenv**, la versión correcta se seleccionará automáticamente al ingresar al directorio del proyecto.

```bash
pyenv install 3.11.5   # Solo si aún no la tenés instalada
pyenv local 3.11.5
```

Verificá la versión con:

```bash
python --version
```
---

```
# Clonar el repo

git clone ...


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

# 1. inicializar alembic en el proyecto
alembic init alembic

# 2. genera una migración automática leyendo tus modelos
alembic revision --autogenerate -m "crear tablas plataforma web "

# 3. aplica la migración en PostgreSQL
alembic upgrade head

# Levantar la API
uvicorn main:app --reload
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
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│   💬 migraciones de base de datos (versionado del esquema)
│
├── app/
│
│   ├── main.py  
│   💬 punto de entrada de la aplicación (fastapi)
│
│   ├── presentation/  🟦 capa de presentación (delivery)
│   │   ├── routers/
│   │   │   └── venta_router.py  
│   │   │   💬 define endpoints rest (http → use cases)
│   │   │
│   │   ├── schemas/
│   │   │   └──venta_schema.py
│   │   │   💬 dtos de entrada/salida (pydantic)
│   │   │
│   │   └── handlers.py
│   │       💬 orquesta requests → casos de uso (opcional desacople de routers)
│   │
│   │   🎯 responsabilidad:
│   │   - recibir requests http
│   │   - validar formato (no reglas de negocio)
│   │   - invocar casos de uso
│
│   ├── application/  🟩 capa de aplicación (use cases)
│   │   │
│   │   ├── dtos
│   │   │   └── venta_dtos.py
│   │   │
│   │   └── use_cases/
│   │       └── validar_stock_venta_use_case.py 
│   │
│   │       💬 implementación de casos de uso del sistema
│   │
│   │   🎯 responsabilidad:
│   │   - orquestar la lógica de negocio
│   │   - coordinar servicios del dominio
│   │   - usar repositorios (a través de puertos)
│   │   - no depende de infraestructura concreta
│
│   ├── domain/  🟥 capa de dominio (core del negocio)
│   │
│   │   ├── models/
│   │   │   ├── detalle_venta.py
│   │   │   ├── producto.py
│   │   │   └── venta.py
│   │   │   💬 entidades y modelos del dominio (reglas puras)
│   │   │
│   │   ├── ports/
│   │   │   ├── i_producto_repository.py
│   │   │   └── i_venta_repository.py
│   │   │   💬 Interfaces (contratos) → patrón Ports & Adapters
│   │   │
│   │   ├── exceptions.py
│   │   │   💬 Excepciones propias del dominio
│   │
│   │   🎯 Responsabilidad:
│   │   - Contener las reglas de negocio
│   │   - Ser independiente de frameworks
│   │   - Definir contratos (ports)
│   
│   ├── infrastructure/  🟨 CAPA DE INFRAESTRUCTURA (Adapters)
│   │
│   │   ├── core/
│   │   │   └── config.py
│   │   │   💬 Configuración global (env, settings)
│   │   │
│   │   ├── database/
│   │   │   ├── session.py
│   │   │   💬 Conexión a la base de datos
│   │   │
│   │   │   ├── orm_models/
│   │   │   │   ├── detalle_venta_orm.py
│   │   │   │   ├── venta_orm.py
│   │   │   │   └── producto_orm.py
│   │   │   │   💬 Modelos ORM (SQLAlchemy)
│   │   │   │
│   │   │   └── repositories/
│   │   │       ├── producto_repository.py
│   │   │       └── venta_repository.py
│   │   │      💬 Implementaciones de los ports (Adapters)
│   │   │   
│   │   │
│   │   │
│   │   ├── dependencies/
│   │   │   └── dependency_injection.py
│   │   │   💬 Inyección de dependencias (wiring de la app)
│   │
│   │   🎯 Responsabilidad:
│   │   - Implementar detalles técnicos (DB, APIs externas)
│   │   - Adaptar interfaces del dominio
│   │   - NO contener lógica de negocio
│   │
│   ├── requirements.txt
│   │
│   │
│   └── tests
│       └── unit
│           ├── fakes
│           │   ├── fake_producto_repository.py
│           │   └── fake_venta_repository.py
│           └── use_cases
│               └── test_validador_stock_venta_use_case.py
│   💬 Tests unitarios del dominio (normalización, validación, etc.)
│
│   🎯 Responsabilidad:
│   - Validar reglas de negocio
│   - Asegurar comportamiento correcto del sistema
│
│
├── README.md  
│   💬 Documentación principal del proyecto
│
└── alembic.ini  
    💬 Configuración de migraciones
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
- Fase 3: Implementación del módulo de productos
- Fase 4: Implementación del módulo de inventario
- Fase 5: Implementación del módulo de ventas
- Fase 6: Implementación del módulo de descuentos
- Fase 7: Implementación del módulo de cambios y devoluciones
- Fase 8: Pruebas unitarias e integración
- Fase 9: Documentación técnica
---

## Tags

- `hu-01-validar-stock-antes-de-vender` 
:+1:



## 🧠 Perfil objetivo

Este proyecto está pensado como material demostrativo para:

---

## Participantes

Emilio Javier Aquino   


## 📄 Licencia

Proyecto de uso educativo y demostrativo.
