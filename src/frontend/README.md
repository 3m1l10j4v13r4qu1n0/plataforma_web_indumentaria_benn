# 📄 README.md para el Frontend de SGVIR

Aquí tienes un README.md profesional y completo, alineado con la arquitectura real del proyecto y las HUs ya implementadas:

```markdown
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
- [Roadmap](#-roadmap)

---

## 🎯 Descripción

El **SGVIR Frontend** es la capa de presentación del Sistema de Gestión de Ventas e Inventario Retail. Proporciona una interfaz web responsiva para que los actores del sistema (Vendedor, Cajero, Gerente) puedan:

- ✅ Procesar ventas con validación de stock en tiempo real
- ✅ Consultar disponibilidad de productos
- ✅ Generar tickets de venta con simulación de impresión
- ✅ Gestionar cambios y devoluciones (validación de tickets y plazos)
- ✅ Controlar descuentos con autorización jerárquica

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

## 🏛️ Arquitectura

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
- ✅ **YAGNI**: No implementar lo que no se necesita aún (ej: autenticación real)
- ✅ **Anti-alucinación**: Solo se consumen endpoints documentados del backend

### Manejo de Errores

- **Interceptor global de Axios** → captura errores HTTP (4xx, 5xx)
- **ErrorBoundary de React** → captura errores de renderizado
- **Cero `try/catch` dispersos** en componentes

---

## 🛠️ Stack Tecnológico

| Categoría | Tecnología | Versión | Justificación |
|---|---|---|---|
| **Build Tool** | Vite | 5.x | Rápido, moderno, configuración mínima |
| **Framework** | React | 18.x | Estándar de la industria |
| **Lenguaje** | TypeScript | 5.x (strict) | Tipado fuerte, evita bugs |
| **Router** | React Router | v6 | Estándar para SPA |
| **HTTP Client** | Axios | 1.x | Interceptores, fácil manejo de errores |
| **Estado API** | TanStack Query | 5.x | Cache, refetch, estados de carga |
| **Estado Global** | Context API | — | Simple, sin dependencias extra |
| **Estilos** | Tailwind CSS | 3.x | Rápido, consistente, utility-first |
| **Testing** | Vitest + RTL | — | Rápido, alineado con Vite |
| **Linting** | ESLint + Prettier | — | Calidad de código |
| **Formularios** | React Hook Form + Zod | — | Validación tipada en el borde |
| **Utilidades** | clsx + tailwind-merge | — | Combinación segura de clases |
| **Fechas** | date-fns | — | Formateo ligero y modular |

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
npm install -D eslint prettier eslint-config-prettier \
  eslint-plugin-react-hooks eslint-plugin-react-refresh
npm install -D @testing-library/react @testing-library/jest-dom \
  @testing-library/user-event
npm install -D vitest jsdom @types/node
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
Abre tu navegador en `http://localhost:5173` y deberías ver la pantalla inicial de Vite + React.

---

```

### Paso 4: Verificar instalación

```bash
npm run dev
```

Abre tu navegador en `http://localhost:5173` y deberías ver la pantalla inicial de Vite + React.

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
curl http://localhost:8000/health
# Debería responder: {"status": "ok"}
```

---

## 📂 Estructura del Proyecto

```
src/frontend/
│
├── index.html                    # HTML principal (entry point)
├── package.json                  # Dependencias y scripts
├── tsconfig.json                 # Configuración TypeScript (strict mode)
├── vite.config.ts                # Configuración Vite + proxy + alias
├── tailwind.config.js            # Configuración Tailwind CSS
├── postcss.config.js             # Configuración PostCSS
├── .prettierrc                   # Configuración Prettier
├── .eslintrc.cjs                 # Configuración ESLint
├── .env                          # Variables de entorno (NO commitear)
├── .env.example                  # Plantilla de variables de entorno
│
├── public/                       # Assets estáticos (favicon, etc.)
│
└── src/
    ├── main.tsx                  # Entry point de React
    ├── App.tsx                   # Componente raíz
    │
    ├── api/                      # 🌐 Capa de comunicación con backend
    │   ├── client.ts             # Instancia de Axios + interceptores
    │   ├── endpoints.ts          # Constantes de URLs oficiales
    │   └── services/             # Servicios por dominio
    │       ├── productos.service.ts
    │       ├── venta.service.ts
    │       └── cambio.service.ts
    │
    ├── components/               # 🎨 Componentes reutilizables
    │   ├── ui/                   # Presentacionales puros (botones, inputs, cards)
    │   │   ├── StockBadge.tsx
    │   │   ├── CartItemRow.tsx
    │   │   ├── ReceiptTicket.tsx
    │   │   ├── PlazoIndicator.tsx
    │   │   └── index.ts          # Barrel export
    │   └── layout/               # Layout (header, error boundary)
    │       ├── PageHeader.tsx
    │       ├── SaleHeader.tsx
    │       ├── ErrorBoundary.tsx
    │       └── index.ts
    │
    ├── pages/                    # 📄 Contenedores (orquestan hooks + UI)
    │   ├── ventas/
    │   │   ├── NuevaVentaPage.tsx
    │   │   └── __tests__/
    │   ├── productos/
    │   │   ├── ConsultarStockPage.tsx
    │   │   └── __tests__/
    │   └── cambios/
    │       ├── GestionCambiosPage.tsx
    │       └── __tests__/
    │
    ├── hooks/                    # 🪝 Custom hooks (lógica de UI)
    │   ├── useCart.ts
    │   ├── useProductSearch.ts
    │   ├── useProcessSale.ts
    │   ├── usePrinter.ts
    │   ├── useCartValidation.ts
    │   ├── __tests__/
    │   └── index.ts
    │
    ├── contexts/                 # 🌍 Contextos globales
    │   └── AuthContext.tsx       # Preparado para auth futura (YAGNI)
    │
    ├── routes/                   # 🧭 Configuración de React Router
    │   ├── AppRouter.tsx
    │   └── ProtectedRoute.tsx
    │
    ├── types/                    # 📝 Tipos TypeScript
    │   ├── api/                  # Espejo de esquemas Pydantic
    │   │   ├── productos.types.ts
    │   │   ├── venta.types.ts
    │   │   ├── ticket.types.ts
    │   │   ├── cambio.types.ts
    │   │   └── error.types.ts
    │   └── domain/               # Tipos de dominio del frontend
    │       ├── producto.types.ts
    │       ├── venta.types.ts
    │       ├── ticket.types.ts
    │       └── cambio.types.ts
    │
    ├── utils/                    # 🛠️ Helpers puros
    │   ├── cn.ts                 # clsx + tailwind-merge
    │   ├── formatCurrency.ts
    │   ├── formatRelativeTime.ts
    │   └── index.ts
    │
    ├── constants/                # 📌 Constantes globales
    │   └── routes.ts
    │
    ├── styles/                   # 🎨 Estilos globales
    │   └── globals.css
    │
    └── test/                     # 🧪 Configuración de testing
        ├── setup.ts
        └── test-utils.tsx
```

---

## 🎬 Scripts Disponibles

| Script | Descripción |
|---|---|
| `npm run dev` | Levanta el servidor de desarrollo en `http://localhost:5173` |
| `npm run build` | Compila la aplicación para producción (en `dist/`) |
| `npm run preview` | Previsualiza el build de producción localmente |
| `npm run test` | Ejecuta todas las pruebas con Vitest |
| `npm run test -- --watch` | Ejecuta pruebas en modo watch |
| `npm run test -- --coverage` | Ejecuta pruebas con reporte de cobertura |
| `npm run lint` | Ejecuta ESLint para verificar calidad de código |
| `npm run format` | Formatea el código con Prettier |

---

## 📏 Convenciones de Código

### Commits Atómicos (Conventional Commits)

```bash
feat: agregar pantalla de procesamiento de ventas
fix: corregir validación de descuento en formulario
refactor: extraer componente de tabla de productos
test: agregar pruebas para hook useBuscarProductos
docs: documentar estructura de carpetas del frontend
chore: actualizar dependencias de Vite
style: aplicar formato con Prettier
```

### Reglas Inquebrantables

- ❌ **Prohibido `any`** en TypeScript
- ❌ **Prohibido inventar endpoints** que no estén en la lista oficial
- ❌ **Prohibido lógica de negocio** en componentes presentacionales
- ❌ **Prohibido `try/catch` dispersos** para errores HTTP
- ❌ **Prohibido autenticación real** hasta que el backend la soporte
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
| HU-06 | Ventas | Consultar stock disponible | ✅ Completada |
| HU-07 | Ventas | Generar ticket de venta | ✅ Completada |
| HU-08 | Inventario | Actualizar stock automáticamente | ✅ Completada (sin UI) |
| HU-04 | Cambios | Solicitar ticket de compra | 🚧 En progreso |
| HU-02 | Cambios | Registrar cambios (15 días) | ⏳ Pendiente |
| HU-03 | Cambios | Validar estado del producto | ⏳ Pendiente |
| HU-05 | Admin | Controlar descuentos | ⏳ Pendiente |

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

### Fase 2: Gestión de Cambios y Devoluciones 🚧
- [ ] HU-04: Solicitar ticket de compra (en progreso)
- [ ] HU-02: Registrar cambios (15 días)
- [ ] HU-03: Validar estado del producto devuelto

### Fase 3: Administración y Control ⏳
- [ ] HU-05: Controlar descuentos (autorización de gerente)

### Futuro
- [ ] Autenticación real (cuando el backend la implemente)
- [ ] Roles y permisos (RBAC)
- [ ] Reportes y dashboards

---

## 🤝 Contribuciones

Este es un proyecto académico. Para contribuir:

1. Crear una rama desde `main`: `git checkout -b feat/nueva-funcionalidad`
2. Seguir los 6 pasos del scaffold para cada HU
3. Asegurar que `npm run lint`, `npm run build` y `npm run test` pasen
4. Hacer commits atómicos siguiendo Conventional Commits
5. Solicitar Pull Request con al menos 1 aprobación

---
