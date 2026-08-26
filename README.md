# plataforma_web_indumentaria_benn

# Sistema de Gestión de Ventas e Inventario Retail (SGVIR)

> **Proyecto Académico de Ingeniería de Software**
> Documentación y desarrollo bajo metodología Ágil (Kanban) y buenas prácticas de TDD y Specification by Example.

---

## 📋 Tabla de Contenidos

- [1. Descripción General](#1-descripción-general)
- [2. Objetivos del Proyecto](#2-objetivos-del-proyecto)
- [3. Alcance](#3-alcance)
- [4. Tecnologías Utilizadas](#4-tecnologías-utilizadas)
- [5. Estructura del Repositorio](#5-estructura-del-repositorio)
- [6. Roadmap del Proyecto](#6-roadmap-del-proyecto)
- [7. Documentación Global Disponible](#7-documentación-global-disponible)
- [8. Arquitectura del Sistema](#8-arquitectura-del-sistema)
- [9. Modelo de Datos (Resumen)](#9-modelo-de-datos-resumen)
- [10. Resumen de Historias de Usuario por Módulo](#10-resumen-de-historias-de-usuario-por-módulo)
- [11. Equipo de Trabajo](#11-equipo-de-trabajo)
- [12. Estado Actual del Proyecto](#12-estado-actual-del-proyecto)
- [13. Próximos Pasos](#13-próximos-pasos)
- [14. Instalación y configuración](#14-instalación-y-configuración)
- [15. Mockups y Prototipos de Interfaz](#15-mockups-y-prototipos-de-interfaz)

---





---

## 1. Descripción General

El **Sistema de Gestión de Ventas e Inventario Retail (SGVIR)** es una solución de software diseñada para modernizar y automatizar los procesos de punto de venta, control de inventario y gestión de post-venta (cambios y devoluciones) en un entorno comercial minorista.

Actualmente, los procesos manuales generan problemas como ventas sin stock real, aplicación de descuentos no autorizados que derivan en pérdidas económicas, y aceptación de cambios de productos usados o fuera del plazo permitido. Este sistema resuelve estas problemáticas mediante validaciones en tiempo real, reglas de negocio estrictas y trazabilidad completa de las operaciones.

---

## 2. Objetivos del Proyecto

### Objetivo General

Desarrollar un sistema integral de punto de venta que garantice la integridad del inventario, el cumplimiento de las políticas comerciales de la empresa y la optimización del tiempo de atención al cliente.

### Objetivos Específicos

1. Validar automáticamente la disponibilidad de stock antes de confirmar cualquier transacción de venta.
2. Automatizar la actualización del inventario (descuento por venta, incremento por devolución) garantizando la consistencia de los datos.
3. Implementar controles estrictos para cambios y devoluciones: validación de ticket obligatorio, plazo máximo de 15 días y estado físico del producto (nuevo y etiquetado).
4. Establecer un sistema de autorización jerárquica para descuentos que superen el porcentaje permitido para el rol de vendedor.

---

## 3. Alcance

**Funcionalidades contempladas (In-Scope):**

- Consulta de stock en tiempo real por código o nombre.
- Proceso de venta con validación previa de stock y generación de comprobante (ticket).
- Flujo completo de cambios/devoluciones: validación de ticket, cálculo de plazo (15 días), inspección de estado del producto y actualización de inventario.
- Control de descuentos con flujo de autorización para gerentes.

**Fuera del alcance (Out-of-Scope):**

- Módulo de comercio electrónico (e-commerce) o venta online.
- Integración con pasarelas de pago externas (simulación de cobro).
- Gestión de proveedores o compras a fábrica.

---

## 4. Tecnologías Utilizadas

- **Arquitectura:** 🏗️ Clean Architecture + Hexagonal Architecture
- **Frontend:** React + TypeScript + Vite, Tailwind CSS.
- **Backend:** Python / FastAPI.
- **Base de Datos:** PostgreSQL (Relacional, para garantizar integridad transaccional ACID).
- **Herramientas de Modelado:** Draw.io / Lucidchart (Diagramas UML y de Flujo).
- **Control de Versiones:** Git y GitHub/GitLab (Monorepo).
- **Gestión de Proyectos:** Trello (Metodología Kanban).

---

## 5. Estructura del Repositorio

El proyecto está organizado como un **Monorepo** para centralizar la documentación y el código, facilitando la trazabilidad entre requisitos e implementación.

```text
plataforma_web_indumentaria_benn/
│
├── README.md                   # Resumen del proyecto, cómo levantar el entorno y enlace a la documentación
├── AGENTS.md                   # Contexto y reglas para asistentes de IA (opencode)
├── opencode.json               # Configuración de opencode
├── .opencode/
│   ├── rules/                  # Reglas del proyecto (stack, negocio, arquitectura, git, estado)
│   └── skills/                 # Skills de scaffolding backend (DI) y frontend (FE)
│
├── docs/                       # Carpeta principal de documentación
│   ├── 01_global/              # 🌍 Información que aplica a TODO el proyecto
│   │   ├── vision.md           # Objetivo del negocio y problema a resolver
│   │   ├── actores.md          # Definición de roles y sus permisos generales
│   │   └── reglas_negocio.md   # 📜 Reglas transversales extraídas de las entrevistas
│   │
│   ├── 02_tecnico/             # ⚙️ Estándares y fundamentos técnicos
│   │   └── modelo_datos_global.md # Entidades base (Producto, Venta, Usuario) que se reutilizan
│   │
│   ├── 03_procesos/            # 🔄 Cómo trabajamos (Kanban)
│   │   └── definicion_listo.md # (DoR) Qué debe tener una HU para pasar a "En Desarrollo"
│   │
│   ├── 04_historias_usuario/   # 📖 Fuente de verdad: una carpeta HU-XX por historia,
│   │   └── HU-01 ... HU-09     #    con especificación, API, modelos de datos y plan de pruebas
│   │
│   └── 05_mockups/             # 🎨 Prototipos HTML + Tailwind por HU (6 mockups)
│
├── src/                        # Carpeta del código (Backend / Frontend)
│   ├── backend/                # API FastAPI — Clean/Hexagonal Architecture (ver src/backend/README.md)
│   └── frontend/               # SPA React + Vite + TypeScript (ver src/frontend/README.md)
│
└── anexo_implementacion_ia/    # Anexos del proceso de implementación con IA

```

---

## 6. Roadmap del Proyecto

Hoja de ruta basada en las Historias de Usuario, agrupadas por módulos funcionales.

### Fase 1: Núcleo de Ventas e Inventario

- [x] [HU-01: Validar stock antes de vender](docs/04_historias_usuario/HU-01/HU-01-validad_stock_anters_de_vender.md)
- [x] [HU-06: Consultar stock disponible](docs/04_historias_usuario/HU-06/HU-06-Consultar_stock_disponible.md)
- [x] [HU-07: Generar ticket de venta](docs/04_historias_usuario/HU-07/HU-07-Generar_ticket_de_venta.md)
- [x] [HU-08: Actualizar stock automáticamente](docs/04_historias_usuario/HU-08/HU-08-Actualizar_stock_automaticamente.md)

### Fase 2: Gestión de Cambios y Devoluciones

- [x] [HU-04: Solicitar ticket de compra (Validación obligatoria)](docs/04_historias_usuario/HU-04/HU-04-Solicitar_ticket_de_compra.md)
- [x] [HU-02: Registrar cambios (Validación de plazo de 15 días)](docs/04_historias_usuario/HU-02/HU-02-Registrar_cambios_de_productos.md)
- [x] [HU-03: Validar estado del producto devuelto](docs/04_historias_usuario/HU-03/HU-03-Validar_estado_del_producto.md)

### Fase 3: Administración y Control

- [x] [HU-05: Controlar descuentos (Límites y autorización de gerente)](docs/04_historias_usuario/HU-05/HU-05-Controlar_descuentos.md)

### Fase 4: Seguridad y Autenticación

- [x] [HU-09: Autenticación JWT y autorización por rol](docs/04_historias_usuario/HU-09-auth/HU-09-autenticacion-jwt.md)

---

## 7. Documentación Global Disponible

| Documento                                                        | Ubicación                                | Descripción                                                                    |
| ---------------------------------------------------------------- | ---------------------------------------- | ------------------------------------------------------------------------------ |
| [Visión y Alcance](docs/01_global/vision.md)                     | `docs/01_global/vision.md`               | Objetivo del negocio y límites del sistema.                                    |
| [Actores del Sistema](docs/01_global/actores.md)                 | `docs/01_global/actores.md`              | Definición de roles (Vendedor, Cajero, Gerente, etc.).                         |
| [Reglas de Negocio](docs/01_global/reglas_negocio.md)            | `docs/01_global/reglas_negocio.md`       | Reglas transversales (ej. plazo de 15 días, stock >= 0).                       |
| [Modelo de Datos Global](docs/02_tecnico/modelo_datos_global.md) | `docs/02_tecnico/modelo_datos_global.md` | Entidades base y relaciones.                                                   |
| [Definition of Ready](docs/03_procesos/definicion_listo.md)      | `docs/03_procesos/definicion_listo.md`   | Criterios para que una HU pase a desarrollo.                                   |
| Detalle HU-01 a HU-09                                            | `docs/04_historias_usuario/HU-XX/`       | Modelos de datos, API, Casos de Uso y Planes de Prueba (TDD/SbE) por historia. |

---

## 8. Arquitectura del Sistema

El sistema sigue una arquitectura en capas de tipo **Cliente-Servidor**:

1. **Frontend**: Aplicación web responsiva que interactúa con el usuario (Vendedor/Cajero). Realiza validaciones de formato en el cliente y consume la API REST.
2. **Backend (API REST)**: Capa de lógica de negocio. Es responsable de aplicar las reglas de negocio estrictas (ej. validación de 15 días, autorización de descuentos), garantizar la seguridad y orquestar las transacciones.
3. **Base de Datos**: Sistema relacional (PostgreSQL) que garantiza la integridad referencial y la atomicidad de las operaciones (transacciones ACID para ventas y actualizaciones de stock).

---

## 9. Modelo de Datos (Resumen)

Las entidades principales del sistema (7 tablas en PostgreSQL):

- **Usuario**: `id`, `email`, `password_hash`, `nombre`, `rol` (VENDEDOR/CAJERO/GERENTE/ENCARGADO_VENTAS), `activo`.
- **Producto**: `id`, `codigo`, `nombre`, `categoria`, `stock_actual` (>=0), `estado`, `precio`.
- **Venta**: `id`, `numero_ticket` (único), `fecha_hora`, `vendedor_id`, `total`, `estado`.
- **Detalle_Venta**: `id`, `venta_id`, `producto_id`, `cantidad`, `precio_unitario`.
- **Descuento**: `id`, `venta_id`, `porcentaje`, `monto_descuento`, `motivo`, `autorizado_por`, `fecha_aplicacion`.
- **Cambio**: `id`, `venta_original_id`, `producto_a_cambiar_id`, `nuevo_producto_id`, `estado`, `motivo`, `fecha_compra_original`, `observaciones`, `fecha_validacion`.
- **Movimiento_Stock**: `id`, `producto_id`, `tipo_movimiento` (VENTA/DEVOLUCION), `cantidad`, `documento_referencia_id`, `fecha_hora`.

---

## 10. Resumen de Historias de Usuario por Módulo

| Módulo         |  HU   | Título                           | Rol Principal    | Valor de Negocio                                                  |
| :------------- | :---: | :------------------------------- | :--------------- | :---------------------------------------------------------------- |
| **Ventas**     | HU-01 | Validar stock antes de vender    | Vendedor         | Evitar ventas de productos inexistentes.                          |
| **Ventas**     | HU-06 | Consultar stock disponible       | Vendedor         | Agilizar la atención al cliente sin ir al depósito.               |
| **Ventas**     | HU-07 | Generar ticket de venta          | Cajero           | Entregar comprobante y mantener registro de operaciones.          |
| **Inventario** | HU-08 | Actualizar stock automáticamente | Encargado Ventas | Mantener la integridad y precisión del inventario en tiempo real. |
| **Cambios**    | HU-04 | Solicitar ticket de compra       | Cajero           | Validar que la venta exista (política de negocio).                |
| **Cambios**    | HU-02 | Registrar cambios (15 días)      | Cajero           | Cumplir con el plazo máximo permitido para cambios.               |
| **Cambios**    | HU-03 | Validar estado del producto      | Vendedor/Cajero  | Aceptar solo productos sin uso y con etiqueta.                    |
| **Admin**      | HU-05 | Controlar descuentos             | Gerente          | Evitar pérdidas económicas por descuentos no autorizados.         |
| **Seguridad**  | HU-09 | Autenticación JWT y autorización | Todos            | Controlar acceso y diferenciar permisos por rol.                  |

---

## 11. Equipo de Trabajo

| Nombre                | Rol en el Proyecto                 | Responsabilidades Principales                                          |
| :-------------------- | :--------------------------------- | :--------------------------------------------------------------------- |
| Aquino, Emilio Javier | Analista Funcional / Product Owner | Relevamiento, redacción de HU, criterios de aceptación.                |
| Brian, Maigua         | Desarrollador Backend              | Diseño de API, modelos de datos, lógica de negocio, TDD.               |
| Nelida, Fernandez     | Desarrollador Frontend             | Implementación de UI/UX, validaciones en cliente, integración con API. |
| Nicol, Vargas         | QA / Tester                        | Diseño de casos de prueba, ejecución de SbE, validación de DoD.        |

---

## 12. Estado Actual del Proyecto

Al día de la fecha, el **alcance funcional definido está implementado** (backend y frontend), con las 9 Historias de Usuario integradas en la rama `develop`.

- ✅ **Relevamiento y Documentación**: 100% Completado. Todas las HU cuentan con su especificación en formato Gherkin, _Specification by Example_ y casos de prueba TDD.
- ✅ **Diseño de Arquitectura y Modelo de Datos**: 100% Completado a nivel conceptual, lógico y físico.
- ✅ **Desarrollo Backend**: FastAPI con Clean/Hexagonal Architecture. 11 endpoints operativos (8 de negocio + 3 de auth), 75 tests unitarios en verde (fakes en memoria, sin DB).
- ✅ **Desarrollo Frontend**: React 19 + Vite + TypeScript. 5 pantallas productivas (`/login`, `/registro`, `/productos/stock`, `/ventas`, `/cambios`) más el modal de descuentos.
- ✅ **Autenticación y Autorización**: JWT (access + refresh token) con 4 roles, protegiendo todos los endpoints.
- ⏳ **Refinamiento**: pendientes opcionales (historial de validaciones por producto, reportes y dashboards).

---

## 13. Próximos Pasos

Basado en el roadmap y la metodología Kanban:

1. **Endpoint opcional de historial**: `GET /api/v1/productos/{producto_id}/validaciones` para consultar inspecciones previas (HU-03).
2. **Reportes y dashboards**: métricas de ventas, cambios y descuentos autorizados.
3. **QA continuo**: mantener suites en verde (pytest backend, Vitest frontend) como criterio de merge.
4. **Tests de integración**: migrar tests unitarios (fakes en memoria) a tests de integración con DB real.
5. **CI/CD**: configurar pipeline de integración continua y despliegue automático.

---

## 14. Instalación y configuración

### **Nota: Para informacion has clic en Backend o Frontend**

- [Backend](src/backend/README.md)
- [Frontend](src/frontend/README.md)

---

## 15. Mockups y Prototipos de Interfaz

Para garantizar que la implementación del Frontend se alinee perfectamente con los requisitos de negocio, se han diseñado prototipos de alta fidelidad en **HTML + Tailwind CSS** para cada Historia de Usuario crítica.

Estos mockups incluyen los estados principales (éxito, error, campos deshabilitados y validaciones) definidos en los criterios de aceptación.

### 📂 Ubicación en el Repositorio

Todos los archivos de los prototipos se encuentran en la carpeta:
`docs/05_mockups/`

### 🖥️ Catálogo de Mockups

| Historia de Usuario | Módulo         | Descripción del Prototipo                                                                                                            | Archivo                 |
| :------------------ | :------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :---------------------- |
| **HU-01**           | Ventas         | Pantalla de punto de venta con validación de stock en tiempo real, badges de color y bloqueo de botón si el stock es 0.              | `mockup_hu01.html`      |
| **HU-02 + HU-04**   | Cambios        | Flujo unificado de validación de ticket y cálculo visual del plazo de 15 días (incluye estados de "plazo válido" y "plazo vencido"). | `mockup_hu02_hu04.html` |
| **HU-03**           | Cambios        | Pantalla de inspección física del producto con checklist de etiqueta, selector de estado y campo de observaciones.                   | `mockup_hu03.html`      |
| **HU-05**           | Administración | Interfaz de aplicación de descuentos con modal de autorización jerárquica para gerentes cuando se supera el límite.                  | `mockup_hu05.html`      |
| **HU-06**           | Consultas      | Pantalla de búsqueda rápida de stock por nombre o código, con indicadores visuales de stock saludable, bajo o agotado.               | `mockup_hu06.html`      |
| **HU-07**           | Ventas         | Pantalla de confirmación de venta con simulación visual de ticket impreso y manejo de errores de impresora.                          | `mockup_hu07.html`      |

### 👁️ Cómo visualizar los mockups

Tienes dos opciones para revisar los diseños:

1. **Localmente (Recomendado)**:
   - Descarga o clona el repositorio.
   - Navega a la carpeta `docs/05_mockups/`.
   - Haz doble clic en cualquier archivo `.html` para abrirlo en tu navegador web (Chrome, Firefox, Edge). No requiere servidor local.

2. **En línea (Tailwind Play)**:
   - Abre el archivo `.html` con un editor de texto (como VS Code o el Bloc de notas).
   - Copia todo el código.
   - Pégalo en [https://play.tailwindcss.com/](https://play.tailwindcss.com/) para verlo renderizado al instante y experimentar con los estados comentados en el código.

_Documento generado para fines académicos. Última actualización: Agosto 2026._
