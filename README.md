# plataforma_web_indumentaria_benn
# Sistema de Gestión de Ventas e Inventario Retail (SGVIR)

> **Proyecto Académico de Ingeniería de Software**  
> Documentación y desarrollo bajo metodología Ágil (Kanban) y buenas prácticas de TDD y Specification by Example.

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
*(Nota: Las siguientes tecnologías son una propuesta estándar para este tipo de arquitectura. [COMPLETAR] con el stack definitivo del equipo).*

- **Frontend:** React.js / Next.js (TypeScript), Tailwind CSS.
- **Backend:** Node.js con NestJS o Express (TypeScript).
- **Base de Datos:** PostgreSQL (Relacional, para garantizar integridad transaccional ACID).
- **Herramientas de Modelado:** Draw.io / Lucidchart (Diagramas UML y de Flujo).
- **Control de Versiones:** Git y GitHub/GitLab (Monorepo).
- **Gestión de Proyectos:** Trello (Metodología Kanban).

---

## 5. Estructura del Repositorio
El proyecto está organizado como un **Monorepo** para centralizar la documentación y el código, facilitando la trazabilidad entre requisitos e implementación.

```text
proyecto-retail/
│
├── README.md                   # Resumen del proyecto, cómo levantar el entorno y enlace a la documentación
│
├── docs/                       # Carpeta principal de documentación
│   ├── 01_global/              # 🌍 Información que aplica a TODO el proyecto
│   │   ├── vision.md           # Objetivo del negocio y problema a resolver
│   │   ├── alcance.md          # Qué incluye esta fase y qué queda fuera (Out of scope)
│   │   ├── actores.md          # Definición de roles y sus permisos generales
│   │   └── reglas_negocio.md   # 📜 Reglas transversales extraídas de las entrevistas
│   │
│   ├── 02_tecnico/             # ⚙️ Estándares y fundamentos técnicos
│   │   ├── arquitectura.md     # Diagrama o descripción de la separación Frontend/Backend
│   │   ├── estandares_api.md   # Convenciones de nombres, códigos HTTP, formato de respuestas
│   │   └── modelo_datos_global.md # Entidades base (Producto, Venta, Usuario) que se reutilizan
│   │
│   ├── 03_procesos/            # 🔄 Cómo trabajamos (Kanban)
│   │   ├── definicion_listo.md # (DoR) Qué debe tener una HU para pasar a "En Desarrollo"
│   │   └── definicion_terminado.md # (DoD) Qué se necesita para mover una HU a "Done"
│   │
│   └── 04_historias_usuario/   # 📂 Aquí irán las carpetas específicas por HU (Fase 2)
│       ├── HU-01/
│       ├── HU-02/
│       └── ...
│
├──src/                        # Carpeta del código (Backend / Frontend)
│  ├── backend/
│  └── frontend/─ database/                       # Scripts de migración, seeders y diseño ER
└── .github/                        # Workflows de CI/CD (si aplica)

```

---

## 6. Roadmap del Proyecto
Hoja de ruta basada en las Historias de Usuario, agrupadas por módulos funcionales.

### Fase 1: Núcleo de Ventas e Inventario
- [x] HU-01: Validar stock antes de vender *(Documentación Completada / Desarrollo: Pendiente)*
- [x] HU-06: Consultar stock disponible *(Documentación Completada / Desarrollo: Pendiente)*
- [x] HU-07: Generar ticket de venta *(Documentación Completada / Desarrollo: Pendiente)*
- [x] HU-08: Actualizar stock automáticamente *(Documentación Completada / Desarrollo: Pendiente)*

### Fase 2: Gestión de Cambios y Devoluciones
- [x] HU-04: Solicitar ticket de compra (Validación obligatoria) *(Documentación Completada / Desarrollo: Pendiente)*
- [x] HU-02: Registrar cambios (Validación de plazo de 15 días) *(Documentación Completada / Desarrollo: Pendiente)*
- [x] HU-03: Validar estado del producto devuelto *(Documentación Completada / Desarrollo: Pendiente)*

### Fase 3: Administración y Control
- [x] HU-05: Controlar descuentos (Límites y autorización de gerente) *(Documentación Completada / Desarrollo: Pendiente)*

---

## 7. Documentación Disponible

| Documento | Ubicación | Descripción |
| --------- | --------- | ----------- |
| Visión y Alcance | `docs/01_global/vision.md` | Objetivo del negocio y límites del sistema. |
| Actores del Sistema | `docs/01_global/actores.md` | Definición de roles (Vendedor, Cajero, Gerente, etc.). |
| Reglas de Negocio | `docs/01_global/reglas_negocio.md` | Reglas transversales (ej. plazo de 15 días, stock >= 0). |
| Modelo de Datos Global | `docs/02_tecnico/modelo_datos_global.md` | Entidades base y relaciones. |
| Definition of Ready | `docs/03_procesos/definicion_listo.md` | Criterios para que una HU pase a desarrollo. |
| Detalle HU-01 a HU-08 | `docs/04_historias_usuario/HU-XX/` | Modelos de datos, API, Casos de Uso y Planes de Prueba (TDD/SbE) por historia. |

---

## 8. Arquitectura del Sistema
El sistema sigue una arquitectura en capas de tipo **Cliente-Servidor**:
1. **Frontend**: Aplicación web responsiva que interactúa con el usuario (Vendedor/Cajero). Realiza validaciones de formato en el cliente y consume la API REST.
2. **Backend (API REST)**: Capa de lógica de negocio. Es responsable de aplicar las reglas de negocio estrictas (ej. validación de 15 días, autorización de descuentos), garantizar la seguridad y orquestar las transacciones.
3. **Base de Datos**: Sistema relacional (PostgreSQL) que garantiza la integridad referencial y la atomicidad de las operaciones (transacciones ACID para ventas y actualizaciones de stock).

---

## 9. Modelo de Datos (Resumen)
Las entidades principales identificadas en el relevamiento son:
- **Usuario**: `id`, `nombre`, `rol` (Vendedor, Cajero, Gerente).
- **Producto**: `id`, `codigo`, `nombre`, `stock_actual` (>=0), `estado`.
- **Venta**: `id`, `numero_ticket` (único), `fecha_hora`, `vendedor_id`, `cajero_id`, `total`, `estado`.
- **Detalle_Venta**: `venta_id`, `producto_id`, `cantidad`, `precio_unitario`.
- **Cambio**: `id`, `venta_original_id`, `fecha_cambio`, `estado_producto` (Nuevo/Usado/Dañado), `tiene_etiqueta` (Boolean), `cajero_id`.
- **Movimiento_Stock**: `id`, `producto_id`, `tipo_movimiento` (VENTA/DEVOLUCION), `cantidad`, `documento_referencia_id`.

---

## 10. Resumen de Historias de Usuario por Módulo

| Módulo | HU | Título | Rol Principal | Valor de Negocio |
| :--- | :---: | :--- | :--- | :--- |
| **Ventas** | HU-01 | Validar stock antes de vender | Vendedor | Evitar ventas de productos inexistentes. |
| **Ventas** | HU-06 | Consultar stock disponible | Vendedor | Agilizar la atención al cliente sin ir al depósito. |
| **Ventas** | HU-07 | Generar ticket de venta | Cajero | Entregar comprobante y mantener registro de operaciones. |
| **Inventario**| HU-08 | Actualizar stock automáticamente | Encargado Ventas | Mantener la integridad y precisión del inventario en tiempo real. |
| **Cambios** | HU-04 | Solicitar ticket de compra | Cajero | Validar que la venta exista (política de negocio). |
| **Cambios** | HU-02 | Registrar cambios (15 días) | Cajero | Cumplir con el plazo máximo permitido para cambios. |
| **Cambios** | HU-03 | Validar estado del producto | Vendedor/Cajero | Aceptar solo productos sin uso y con etiqueta. |
| **Admin** | HU-05 | Controlar descuentos | Gerente | Evitar pérdidas económicas por descuentos no autorizados. |

---

## 11. Equipo de Trabajo
*(Nota: [COMPLETAR] con los datos reales del equipo académico)*

| Nombre | Rol en el Proyecto | Responsabilidades Principales |
| :--- | :--- | :--- |
| [Nombre Apellido] | Analista Funcional / Product Owner | Relevamiento, redacción de HU, criterios de aceptación. |
| [Nombre Apellido] | Desarrollador Backend | Diseño de API, modelos de datos, lógica de negocio, TDD. |
| [Nombre Apellido] | Desarrollador Frontend | Implementación de UI/UX, validaciones en cliente, integración con API. |
| [Nombre Apellido] | QA / Tester | Diseño de casos de prueba, ejecución de SbE, validación de DoD. |

---

## 12. Estado Actual del Proyecto
Al día de la fecha, el proyecto se encuentra en la fase de **Transición de Ingeniería de Requisitos a Desarrollo**. 
- ✅ **Relevamiento y Documentación**: 100% Completado. Todas las HU cuentan con su especificación en formato Gherkin, *Specification by Example* y casos de prueba TDD.
- ✅ **Diseño de Arquitectura y Modelo de Datos**: 100% Completado a nivel conceptual y lógico.
- ⏳ **Desarrollo de Software**: 0% Iniciado (Listo para comenzar con la HU-01 según el tablero Kanban).

---

## 13. Próximos Pasos
Basado en el roadmap y la metodología Kanban, las tareas inmediatas son:

1. **Configuración del Entorno**: Inicializar el monorepo, configurar linters, formatters y la base de datos local de desarrollo.
2. **Implementación de HU-01 (Prioridad Alta)**: 
   - Backend: Crear entidad `Producto` y endpoint de validación de stock.
   - Frontend: Implementar la vista de venta con indicador visual de stock.
   - QA: Ejecutar los casos de prueba TDD definidos en `docs/04_historias_usuario/HU-01/HU-01_pruebas.md`.
3. **Revisión de Código**: Establecer el flujo de Pull Requests con al menos una aprobación requerida antes de fusionar a la rama principal.

---

## 14.

---

## 15. Mockups y Prototipos de Interfaz

Para garantizar que la implementación del Frontend se alinee perfectamente con los requisitos de negocio, se han diseñado prototipos de alta fidelidad en **HTML + Tailwind CSS** para cada Historia de Usuario crítica. 

Estos mockups incluyen los estados principales (éxito, error, campos deshabilitados y validaciones) definidos en los criterios de aceptación.

### 📂 Ubicación en el Repositorio
Todos los archivos de los prototipos se encuentran en la carpeta:  
`docs/05_mockups/`

### 🖥️ Catálogo de Mockups

| Historia de Usuario | Módulo | Descripción del Prototipo | Archivo |
| :--- | :--- | :--- | :--- |
| **HU-01** | Ventas | Pantalla de punto de venta con validación de stock en tiempo real, badges de color y bloqueo de botón si el stock es 0. | `mockup_hu01.html` |
| **HU-02 + HU-04** | Cambios | Flujo unificado de validación de ticket y cálculo visual del plazo de 15 días (incluye estados de "plazo válido" y "plazo vencido"). | `mockup_hu02_hu04.html` |
| **HU-03** | Cambios | Pantalla de inspección física del producto con checklist de etiqueta, selector de estado y campo de observaciones. | `mockup_hu03.html` |
| **HU-05** | Administración | Interfaz de aplicación de descuentos con modal de autorización jerárquica para gerentes cuando se supera el límite. | `mockup_hu05.html` |
| **HU-06** | Consultas | Pantalla de búsqueda rápida de stock por nombre o código, con indicadores visuales de stock saludable, bajo o agotado. | `mockup_hu06.html` |
| **HU-07** | Ventas | Pantalla de confirmación de venta con simulación visual de ticket impreso y manejo de errores de impresora. | `mockup_hu07.html` |

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

> **Nota para el equipo de desarrollo**: Los mockups contienen comentarios HTML (`<!-- REQ: ... -->`) que vinculan directamente cada elemento visual con el criterio de aceptación específico de la Historia de Usuario correspondiente.---

*Documento generado para fines académicos. Última actualización: Junio 2026.*
```

### 💡 Notas sobre el uso de este README:
1. **Reemplaza los marcadores `[COMPLETAR]`** en las secciones de Tecnologías y Equipo con la información real de tu grupo de trabajo.
2. Este archivo está diseñado para ser la **portada de tu repositorio**. Al subirlo a GitHub/GitLab, renderizará perfectamente con la tabla de contenidos, las listas de verificación y la estructura de árbol.
3. Refleja fielmente el trabajo que hicimos juntos: separación de responsabilidades, enfoque en Kanban y un nivel de detalle profesional en los requisitos.
