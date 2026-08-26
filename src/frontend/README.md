# 📄 README.md para el Frontend de SGVIR

# 🛍️ SGVIR Frontend — Sistema de Gestión de Ventas e Inventario Retail

> **Proyecto Académico de Ingeniería de Software**
> Frontend en React + TypeScript + Vite para el sistema retail SGVIR.
> Metodología Ágil (Kanban) + TDD + Specification by Example.

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Arquitectura](#-arquitectura)
- [Stack Tecnológico](#-stack-tecnológico)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación desde Cero](#-instalación-desde-cero)
- [Clonar el Repositorio](#-clonar-el-repositorio)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Scripts Disponibles](#-scripts-disponibles)
- [Convenciones de Código](#-convenciones-de-código)
- [Estado del Proyecto](#-estado-del-proyecto)
- [Roadmap](#️-roadmap)

---

## 🎯 Descripción

El **SGVIR Frontend** es la capa de presentación del Sistema de Gestión de Ventas e Inventario Retail. Proporciona una interfaz web responsiva para que los actores del sistema (Vendedor, Cajero, Gerente) puedan:

- ✅ Procesar ventas con validación de stock en tiempo real
- ✅ Consultar disponibilidad de productos
- ✅ Generar tickets de venta con simulación de impresión
- ✅ Gestionar cambios y devoluciones (validación de tickets y plazos)
- ✅ Controlar descuentos con autorización jerárquica
- ✅ Autenticarse con JWT (login, registro, roles)

### 🏗️ Relación con el Backend

Este frontend consume una API REST construida con **FastAPI + Clean Architecture + Hexagonal**, que implementa la lógica de negocio estricta (reglas de stock, plazos de cambio, autorizaciones).

```
┌─────────────────┐         ┌─────────────────┐         ┌──────────────┐
│   Frontend      │  HTTP   │   Backend       │  SQL    │  PostgreSQL  │
│   React + Vite  │ ◄─────► │   FastAPI       │ ◄─────► │              │
│   TypeScript    │  JSON   │   Hexagonal     │         │              │
└─────────────────┘         └─────────────────┘         └──────────────┘
```

---

## 🎯 Arquitectura

El frontend sigue los principios de **Clean Architecture adaptados a React**, con estricta separación de responsabilidades:

### Capas

| Capa | Ubicación | Responsabilidad |
|---|---|---|
| **Presentación (UI)** | `src/components/ui/`, `src/components/layout/` | Componentes puros, solo reciben props y renderizan |
| **Contenedores (Pages)** | `src/pages/` | Orquestan hooks y componentes, manejan estados universales |
| **Lógica de UI (Hooks)** | `src/hooks/` | Encapsulan llamadas HTTP, estado local, TanStack Query |
| **Servicios API** | `src/api/services/` | Única capa que conoce endpoints y formatos del backend |
| **Tipos** | `src/types/` | Tipos TypeScript espejo de esquemas Pydantic |

### Principios Aplicados

- ✅ **SRP**: Cada componente/hook tiene una única responsabilidad
- ✅ **DIP**: Los contenedores dependen de hooks, no de Axios directamente
- ✅ **KISS**: Solución más simple posible, sin sobre-ingeniería
- ✅ **DRY**: Componentes y hooks reutilizables
- ✅ **YAGNI**: No implementar lo que no se necesita aún
- ✅ **Anti-alucinación**: Solo se consumen endpoints documentados del backend

### Manejo de Errores

- **Interceptor global de Axios** → captura errores HTTP (4xx, 5xx)
- **ErrorBoundary de React** → captura errores de renderizado
- **Cero `try/catch` dispersos** en componentes

---

## 🎯 Stack Tecnológico

| Categoría | Tecnología | Versión | Justificación |
|---|---|---|---|
| **Build Tool** | Vite | 8.x | Rápido, moderno, configuración mínima |
| **Framework** | React | 19.x | Estándar de la industria |
| **Lenguaje** | TypeScript | 6.x (strict) | Tipado fuerte, evita bugs |
| **Router** | React Router | v7 | Estándar para SPA |
| **HTTP Client** | Axios | 1.x | Interceptores, fácil manejo de errores |
| **Estado API** | TanStack Query | 5.x | Cache, refetch, estados de carga |
| **Estado Global** | Context API | — | Simple, sin dependencias extra |
| **Estilos** | Tailwind CSS | 4.x (plugin Vite) | Rápido, consistente, utility-first |
| **Testing** | Vitest + RTL | — | Rápido, alineado con Vite |
| **Linting** | oxlint | — | Calidad de código (config en `.oxlintrc.json`) |
| **Formularios** | React Hook Form + Zod | — | Validación tipada en el borde |
| **Utilidades** | clsx + tailwind-merge | — | Combinación segura de clases |
| **Fechas** | date-fns | — | Formateo ligero y modular |

> ⚠️ Tailwind v4 no usa `tailwind.config.js` ni `postcss.config.js`: la configuración de tema vive en el CSS con `@theme`. El lint es **oxlint** (`npm run lint`); no hay script `format`.

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

| Herramienta | Versión Mínima | Verificar |
|---|---|---|
| **Node.js** | 18.x o superior | `node --version` |
| **npm** | 9.x o superior | `npm --version` |
| **Git** | 2.x o superior | `git --version` |

> 💡 **Recomendado**: Usa [nvm](https://github.com/nvm-sh/nvm) para gestionar versiones de Node.js.

---
## 🚀 Instalación desde Cero
Si estás creando el proyecto desde cero (no clonando):

### Paso 1: Crear el proyecto con Vite
```bash
# Posicionarse en la carpeta src del monorepo
cd src
# Crear el proyecto frontend con Vite (React + TypeScript)
npm create vite@latest frontend -- --template react-ts
# Entrar al proyecto
cd frontend
# Instalar dependencias base
npm install
```

### Paso 2: Instalar dependencias del stack
```bash
# Routing
npm install react-router-dom
# HTTP Client
npm install axios
# Formularios + Validación
npm install react-hook-form @hookform/resolvers zod
# Estado global de API
npm install @tanstack/react-query
# Utilidades
npm install clsx tailwind-merge date-fns
# Tailwind CSS v4 + plugin de Vite
npm install tailwindcss @tailwindcss/vite
# Dev dependencies
npm install -D oxlint @vitejs/plugin-react
npm install -D @testing-library/react @testing-library/jest-dom \
  @testing-library/user-event
npm install -D vitest jsdom @types/node typescript
```

### Paso 3: Configurar Tailwind CSS v4
Agregar el plugin en `vite.config.ts`:
```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
})
```

Reemplazar el contenido de `src/index.css`:
```css
@import "tailwindcss";
```

> ⚠️ Tailwind v4 no requiere `tailwind.config.js` ni `postcss.config.js`.
> La configuración de tema se hace directamente en el CSS con `@theme`.

### Paso 4: Verificar instalación
```bash
npm run dev
```
Abre tu navegador en `http://localhost:5173` y deberías ver la pantalla inicial.

---

## 📥 Clonar el Repositorio

Si ya existe el repositorio y vas a clonarlo:

### Paso 1: Clonar el monorepo

```bash
# Clonar el repositorio completo
git clone https://github.com/3m1l10j4v13r4qu1n0/plataforma_web_indumentaria_benn/

# Entrar al repositorio
cd plataforma_web_indumentaria_benn
```

### Paso 2: Instalar dependencias del frontend

```bash
# Navegar a la carpeta del frontend
cd src/frontend

# Instalar todas las dependencias
npm install
```

### Paso 3: Configurar variables de entorno

Crear un archivo `.env` en `src/frontend/` (copiar de `.env.example` si existe):

```bash
cp .env.example .env
```

Contenido típico del `.env`:

```env
# URL base de la API del backend
VITE_API_BASE_URL=http://localhost:8000
```

### Paso 4: Levantar el backend (requerido)

El frontend necesita el backend corriendo para funcionar:

```bash
# Desde la raíz del monorepo
cd src/backend

# Instalar dependencias del backend (primera vez)
pip install -r requirements.txt

# Levantar el servidor FastAPI
uvicorn app.main:app --reload --port 8000
```

### Paso 5: Levantar el frontend

En otra terminal:

```bash
# Desde src/frontend
npm run dev
```

Abre tu navegador en `http://localhost:5173` 🎉

### Paso 6: Verificar conexión

El frontend está configurado con un proxy en `vite.config.ts` que redirige las peticiones `/api/*` al backend. Verifica que todo funciona:

```bash
# Desde src/frontend
curl http://localhost:8000/
# Debería responder: {"estado": "ok", ...}
# (El health check del backend es GET / — NO existe /health)
```

---

## 📂 Estructura del Proyecto

```
src/frontend/
│
├── index.html                    # HTML principal (entry point)
├── package.json                  # Dependencias y scripts
├── tsconfig.json                 # Configuración TypeScript (strict mode)
├── vite.config.ts                # Configuración Vite + proxy + alias + Vitest
├── .oxlintrc.json                # Configuración de oxlint (linter)
├── .prettierrc                   # Configuración Prettier
├── .env                          # Variables de entorno (NO commitear)
├── .env.example                  # Plantilla de variables de entorno
│
├── public/                       # Assets estáticos (favicon, etc.)
│
└── src/
    ├── main.tsx                  # Entry point de React (QueryClient + Router)
    │
    ├── api/                      # 🌐 Capa de comunicación con backend
    │   ├── client.ts             # Instancia de Axios + interceptores
    │   ├── endpoints.ts          # Constantes de URLs oficiales
    │   └── services/             # Servicios por dominio
    │       ├── productos.service.ts        # Consulta y búsqueda de stock (HU-06)
    │       ├── productos.service.types.ts  # Contrato IProductosService
    │       ├── venta.service.ts            # Procesar venta / ticket (HU-01/07)
    │       ├── cambio.service.ts           # Flujo de cambios (HU-02/03/04)
    │       ├── descuento.service.ts        # Descuentos con autorización (HU-05)
    │       └── auth.service.ts             # Login, registro, refresh (HU-09)
    │
    ├── components/               # 🎨 Componentes reutilizables
    │   ├── ui/                   # Presentacionales puros (reciben props y renderizan)
    │   │   ├── Alert.tsx, Button.tsx, Toast.tsx, EmptyState.tsx
    │   │   ├── StockBadge.tsx, StockSearchInput.tsx, ProductoBusquedaCard.tsx
    │   │   ├── VentaProductoCard.tsx, VentaItemRow.tsx, ResultsHeader.tsx
    │   │   ├── TicketSearchInput.tsx, TicketCard.tsx, CompraOriginalCard.tsx
    │   │   ├── RegistroCambioForm.tsx, EstadoProductoSelector.tsx
    │   │   ├── CambioExitosoCard.tsx, DescuentoModal.tsx
    │   │   └── index.ts          # Barrel export
    │   └── layout/               # Layout (header)
    │       ├── PageHeader.tsx
    │       └── index.ts
    │
    ├── pages/                    # 📄 Contenedores (orquestan hooks + UI)
    │   ├── auth/
    │   │   ├── LoginPage.tsx             # Formulario de login (HU-09)
    │   │   └── RegisterPage.tsx          # Formulario de registro (HU-09)
    │   ├── ventas/
    │   │   ├── CrearVentaPage.tsx
    │   │   └── __tests__/
    │   ├── productos/
    │   │   ├── ConsultarStockPage.tsx
    │   │   └── __tests__/
    │   └── cambios/
    │       ├── RegistrarCambioPage.tsx     # Wizard completo (HU-02/03/04)
    │       └── __tests__/
    │
    ├── hooks/                    # 🪝 Custom hooks (lógica de UI)
    │   ├── useStockProducto.ts
    │   ├── useBuscarProductos.ts
    │   ├── useVenta.ts
    │   ├── useTicket.ts
    │   ├── useMarcarVentaEnCambio.ts
    │   ├── useCambio.ts
    │   └── useDescuento.ts
    │
    ├── contexts/                 # 🌍 Contextos globales
    │   └── AuthContext.tsx       # Auth activo: login, logout, JWT, sesion (HU-09)
    │
    ├── routes/                   # 🧭 Configuración de React Router v7
    │   ├── AppRouter.tsx         # /login · /registro · /productos/stock · /ventas · /cambios
    │   └── ProtectedRoute.tsx    # Guard de rutas autenticadas (HU-09)
    │
    ├── types/                    # 📝 Tipos TypeScript
    │   ├── api/                  # Espejo de esquemas Pydantic
    │   │   ├── productos.types.ts
    │   │   ├── venta.types.ts
    │   │   ├── cambio.types.ts
    │   │   ├── descuento.types.ts
    │   │   ├── auth.types.ts             # Tipos de auth (HU-09)
    │   │   ├── error.types.ts
    │   │   └── index.ts
    │   └── domain/               # Tipos de dominio del frontend
    │
    ├── utils/                    # 🛠️ Helpers puros
    │   ├── cn.ts                 # clsx + tailwind-merge
    │   ├── format.ts             # Formateo de moneda/fechas
    │   └── apiErrors.ts          # Normalización de errores de API
    │
    ├── constants/                # 📌 Constantes globales
    │   ├── routes.ts
    │   └── stock.ts              # Umbrales de niveles de stock
    │
    ├── index.css                 # 🎨 Tailwind v4 (@theme con colores brand)
    │
    └── test/                     # 🧪 Configuración de testing
        └── setup.ts
```

---

## 🎬 Scripts Disponibles

| Script | Descripción |
|---|---|
| `npm run dev` | Levanta el servidor de desarrollo en `http://localhost:5173` |
| `npm run build` | Compila la aplicación para producción (`tsc -b && vite build`, en `dist/`) |
| `npm run preview` | Previsualiza el build de producción localmente |
| `npm run test` | Ejecuta todas las pruebas con Vitest |
| `npm run test:ui` | Ejecuta las pruebas con la interfaz visual de Vitest |
| `npm run test -- --watch` | Ejecuta pruebas en modo watch |
| `npm run lint` | Ejecuta oxlint para verificar calidad de código |

---

## 📏 Convenciones de Código

### Commits Atómicos (Conventional Commits)

```bash
feat(ventas): se agrega pantalla de procesamiento de ventas
fix(descuentos): se corrige validacion de descuento en formulario
refactor(productos): se extrae componente de tabla de productos
test(hooks): se agregan pruebas para hook useBuscarProductos
docs: se documenta estructura de carpetas del frontend
chore: se actualizan dependencias de Vite
```

### Reglas Inquebrantables

- ❌ **Prohibido `any`** en TypeScript
- ❌ **Prohibido inventar endpoints** que no estén en la lista oficial
- ❌ **Prohibido lógica de negocio** en componentes presentacionales
- ❌ **Prohibido `try/catch` dispersos** para errores HTTP
- ✅ **Componentes pequeños** (<150 líneas)
- ✅ **Nombres descriptivos** para componentes, hooks y variables
- ✅ **Tipos alineados** con esquemas Pydantic del backend

### Checklist Pre-Commit

```bash
[ ] npm run lint sin errores
[ ] npm run build compila correctamente
[ ] npm run test todas las pruebas pasan
[ ] No hay console.log de debug
[ ] No hay código comentado innecesario
[ ] Los tipos reflejan exactamente los esquemas Pydantic
```

---

## 📊 Estado del Proyecto

### Historias de Usuario Implementadas

| HU | Módulo | Título | Estado Frontend |
|---|---|---|---|
| HU-01 | Ventas | Validar stock antes de vender | ✅ Completada |
| HU-02 | Cambios | Registrar cambios (15 días) | ✅ Completada |
| HU-03 | Cambios | Validar estado del producto | ✅ Completada |
| HU-04 | Cambios | Solicitar ticket de compra | ✅ Completada |
| HU-05 | Admin | Controlar descuentos | ✅ Completada (modal) |
| HU-06 | Ventas | Consultar stock disponible | ✅ Completada |
| HU-07 | Ventas | Generar ticket de venta | ✅ Completada |
| HU-08 | Inventario | Actualizar stock automáticamente | ✅ Completada (feedback post-venta) |
| HU-09 | Seguridad | Autenticación JWT y autorización | ✅ Completada (login, registro, ProtectedRoute) |

Pantallas activas en el router: `/login`, `/registro`, `/productos/stock`, `/ventas` y `/cambios`.

### Flujo de Trabajo (6 Pasos por HU)

Cada HU se implementa siguiendo estrictamente estos pasos:

1. **Tipos y Contratos** → Tipos TypeScript espejo de Pydantic
2. **Configuración de Rutas** → Registrar en `AppRouter.tsx`
3. **Componentes Presentacionales** → UI pura en `src/components/ui/`
4. **Custom Hooks** → Lógica de UI en `src/hooks/`
5. **Página/Contenedor** → Orquestación en `src/pages/`
6. **Pruebas de Componentes** → Vitest + React Testing Library

---

## 🗺️ Roadmap

### Fase 1: Núcleo de Ventas e Inventario ✅
- [x] HU-01: Validar stock antes de vender
- [x] HU-06: Consultar stock disponible
- [x] HU-07: Generar ticket de venta
- [x] HU-08: Actualizar stock automáticamente

### Fase 2: Gestión de Cambios y Devoluciones ✅
- [x] HU-04: Solicitar ticket de compra
- [x] HU-02: Registrar cambios (15 días)
- [x] HU-03: Validar estado del producto devuelto

### Fase 3: Administración y Control ✅
- [x] HU-05: Controlar descuentos (autorización de gerente)

### Fase 4: Seguridad y Autenticación ✅
- [x] HU-09: Autenticación JWT (login, registro, ProtectedRoute, AuthContext)

### Futuro
- [ ] Reportes y dashboards
- [ ] Tests de integración con backend real

---

## 🤝 Contribuciones

Este es un proyecto académico. Para contribuir:

1. Crear una rama desde `develop`: `git checkout -b feat/nueva-funcionalidad`
2. Seguir los 6 pasos del scaffold para cada HU
3. Asegurar que `npm run lint`, `npm run build` y `npm run test` pasen
4. Hacer commits atómicos siguiendo Conventional Commits (en español, ver `.opencode/rules/flujo-git.md`)
5. Solicitar Pull Request con al menos 1 aprobación

---
