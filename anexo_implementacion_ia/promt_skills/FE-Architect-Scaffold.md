# 🎨 Skill: FE-Architect-Scaffold

## 🎯 Propósito
Estandarizar la implementación del frontend en **React.js + Vite + TypeScript**, garantizando una arquitectura escalable, bajo acoplamiento con la UI, y **alineación estricta con el backend existente** (FastAPI + Clean Architecture).

Este skill actúa como un **contrato de no-alucinación**: el agente de IA NO puede inventar endpoints, tipos ni comportamientos que no estén documentados en el backend.

---

## 📜 Reglas Inquebrantables del Frontend (SFAV)

### 1. Fuente Única de Verdad: El Backend
- **Prohibido inventar endpoints**: Solo se pueden consumir los endpoints documentados en el backend (ver lista oficial abajo).
- **Prohibido inventar campos en las respuestas**: Los tipos TypeScript deben reflejar **exactamente** los esquemas Pydantic del backend.
- **Prohibido inventar códigos de error**: Solo se manejan los errores que el backend devuelve vía `handlers.py`.

### 2. Separación de Responsabilidades
- **Componentes Presentacionales (UI)**: Solo reciben props y renderizan. NO hacen llamadas HTTP ni manejan estado global.
- **Componentes Contenedores (Pages/Containers)**: Orquestan datos, llaman a servicios/API y pasan props a los presentacionales.
- **Custom Hooks**: Encapsulan lógica reutilizable (llamadas HTTP, estado local complejo).
- **Servicios/API Client**: Única capa que conoce los endpoints y formatos del backend.

### 3. Manejo Centralizado de Errores HTTP
- Prohibido usar `try/catch` dispersos en componentes para errores de API.
- Todos los errores HTTP (400, 403, 404, 409, 500) deben manejarse en un **interceptor global de Axios** o un **ErrorBoundary** de React.
- Los errores de negocio del backend (ej. `STOCK_INSUFICIENTE`, `PLAZO_DE_CAMBIO_VENCIDO`) deben mapearse a mensajes amigables para el usuario.

### 4. Tipado Estricto con TypeScript
- `tsconfig.json` debe tener `"strict": true`.
- Prohibido usar `any`. Si un tipo no está claro, se define explícitamente.
- Los tipos de respuesta de API deben vivir en `src/types/api/` y reflejar los esquemas Pydantic.

### 5. Estructura de Carpetas Estricta
Respetar la siguiente estructura sin desviaciones:

```
src/
├── api/                    # Cliente HTTP y configuración
│   ├── client.ts           # Instancia de Axios con interceptores
│   ├── endpoints.ts        # Constantes de URLs (evita strings mágicos)
│   └── services/           # Funciones por dominio (venta, producto, cambio)
│       ├── venta.service.ts
│       ├── producto.service.ts
│       └── cambio.service.ts
├── components/             # Componentes reutilizables (presentacionales)
│   ├── ui/                 # Botones, inputs, modales, cards
│   └── layout/             # Header, Footer, Sidebar
├── pages/                  # Páginas (contenedores que orquestan)
│   ├── ventas/
│   ├── productos/
│   └── cambios/
├── hooks/                  # Custom hooks (useVentas, useProductos, etc.)
├── contexts/               # Contextos globales (AuthContext, ThemeContext)
├── routes/                 # Configuración de React Router
│   ├── AppRouter.tsx
│   └── ProtectedRoute.tsx  # Preparado para autenticación futura
├── types/                  # Tipos TypeScript
│   ├── api/                # Tipos de respuesta de API (espejo de Pydantic)
│   └── domain/             # Tipos de dominio del frontend
├── utils/                  # Helpers puros (formateo de fechas, validaciones)
├── constants/              # Constantes globales
├── styles/                 # Estilos globales (si no se usa Tailwind)
└── App.tsx                 # Componente raíz
```

### 6. Estado Global (YAGNI)
- **No usar Redux** a menos que sea estrictamente necesario.
- Para estado global simple: **Context API + useReducer**.
- Para estado global complejo futuro: considerar **Zustand** (más simple que Redux).
- Para datos de API: **TanStack Query (React Query)** es recomendado para cache, refetch y estados de carga/error.

### 7. Preparación para Autenticación (Fase Futura)
Aunque el backend aún no tiene autenticación implementada, el frontend debe estar **preparado** para integrarla sin refactorizaciones masivas:
- Crear un `AuthContext` vacío con la estructura básica (user, token, login, logout).
- Crear un `ProtectedRoute` que redirija a `/login` si no hay token.
- Configurar el interceptor de Axios para inyectar el header `Authorization: Bearer <token>` cuando exista.
- **NO implementar login real todavía** (YAGNI): solo dejar la estructura lista.

---

## 🔄 Flujo de Trabajo Estándar (6 Pasos)

Cada vez que se solicite implementar una nueva pantalla o funcionalidad del frontend, se debe seguir estrictamente este orden:

### Paso 1: Definición de Tipos y Contratos (API Layer)
**Ubicación**: `src/types/api/` y `src/api/services/`
**Acciones**:
- Crear los tipos TypeScript que reflejen los esquemas Pydantic del backend (Request y Response).
- Crear la función del servicio que consumirá el endpoint correspondiente.
- **Validación**: Comparar línea por línea con el esquema Pydantic del backend. Si hay discrepancia, DETENER y consultar.

### Paso 2: Configuración de Rutas
**Ubicación**: `src/routes/`
**Acciones**:
- Agregar la nueva ruta en `AppRouter.tsx`.
- Si la pantalla requiere autenticación (futuro), envolverla en `ProtectedRoute`.
- Definir la ruta en `endpoints.ts` si es un path del frontend.

### Paso 3: Componentes Presentacionales (UI)
**Ubicación**: `src/components/ui/`
**Acciones**:
- Crear los componentes visuales reutilizables (botones, formularios, tablas, cards).
- Deben recibir **solo props tipadas**, sin lógica de negocio.
- Aplicar estilos consistentes (Tailwind o CSS Modules).

### Paso 4: Custom Hooks (Lógica de UI)
**Ubicación**: `src/hooks/`
**Acciones**:
- Crear hooks como `useVentas`, `useProductos`, `useBuscarProductos`.
- El hook encapsula: estado de carga, estado de error, datos, y la llamada al servicio.
- Si se usa TanStack Query, el hook envuelve `useQuery` o `useMutation`.

### Paso 5: Página/Contenedor (Orquestación)
**Ubicación**: `src/pages/`
**Acciones**:
- Crear la página que consume el hook y renderiza los componentes presentacionales.
- Manejar los tres estados universales: **Loading**, **Error**, **Success**.
- NO hacer llamadas HTTP directamente aquí; delegar al hook.

### Paso 6: Pruebas de Componentes
**Ubicación**: `src/__tests__/` o junto al componente (`*.test.tsx`)
**Acciones**:
- Usar **Vitest + React Testing Library**.
- Probar comportamiento, no implementación (ej. "al hacer clic se muestra el modal", no "se llama a setState").
- Mockear los servicios API con `vi.mock()`.

---

## 📋 Lista Oficial de Endpoints del Backend (Anti-Alucinación)

**⚠️ REGLA DE ORO**: Solo se pueden consumir estos endpoints. Si necesitas uno que no está aquí, **DETÉN la implementación y consulta al usuario**.

| Método | Endpoint | Propósito | HU Asociada |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/ventas` | Procesar venta (valida stock, descuentos) | HU-01, HU-05, HU-07, HU-08 |
| `GET` | `/api/v1/productos/{codigo}/stock` | Consultar stock de un producto | HU-01 |
| `GET` | `/api/v1/productos/buscar?query=...` | Buscar productos por nombre/código | HU-06 |
| `GET` | `/api/v1/ventas/tickets/{numero_ticket}` | Consultar detalles de un ticket | HU-04 |
| `POST` | `/api/v1/cambios/validar-elegibilidad` | Validar si un ticket/producto es elegible para cambio | HU-02, HU-03, HU-04 |
| `GET` | `/health` | Health check del sistema | - |

### 📦 Estructura de Respuestas de Error del Backend

Todos los errores siguen este formato JSON (definido en `handlers.py`):

```typescript
// src/types/api/error.types.ts
export interface ApiErrorResponse {
  error: string;          // Código de error (ej. "STOCK_INSUFICIENTE")
  mensaje: string;        // Mensaje descriptivo
  producto_id?: string;   // Campo contextual (puede variar)
  numero_ticket?: string;
  usuario_id?: string;
}
```

### 🚦 Códigos HTTP y su Significado

| Código | Significado | Acción en Frontend |
| :--- | :--- | :--- |
| `200` | Éxito (GET, PUT) | Mostrar datos |
| `201` | Creado (POST) | Mostrar confirmación + redirigir si aplica |
| `400` | Error de validación / regla de negocio | Mostrar mensaje al usuario |
| `403` | No autorizado (ej. descuento sin gerente) | Mostrar mensaje específico |
| `404` | Recurso no encontrado | Mostrar "No encontrado" |
| `409` | Conflicto (ej. stock insuficiente) | Mostrar conflicto y ofrecer alternativa |
| `500` | Error interno del servidor | Mostrar "Error inesperado, contacte soporte" |

---

## 🛠️ Stack Tecnológico Recomendado

| Categoría | Tecnología | Justificación |
| :--- | :--- | :--- |
| Build Tool | **Vite** | Rápido, moderno, configuración mínima |
| Framework | **React 18+** | Estándar de la industria |
| Lenguaje | **TypeScript (strict)** | Tipado fuerte, evita bugs |
| Router | **React Router v6** | Estándar para SPA |
| HTTP Client | **Axios** | Interceptores, fácil manejo de errores |
| Estado API | **TanStack Query (opcional)** | Cache, refetch, estados de carga |
| Estado Global | **Context API + useReducer** | Simple, sin dependencias extra |
| Estilos | **Tailwind CSS** | Rápido, consistente, utility-first |
| Testing | **Vitest + React Testing Library** | Rápido, alineado con Vite |
| Linting | **ESLint + Prettier** | Calidad de código |
| Formularios | **React Hook Form + Zod** | Validación tipada en el borde |

---

## 🌱 Cultura de Desarrollo (Developer Culture)

### Principios Aplicados
- **Clean Code**: Nombres descriptivos, componentes pequeños (<150 líneas).
- **SOLID**: SRP en componentes, DIP en servicios.
- **KISS**: No sobre-ingenierizar. Si un `div` basta, no crear un componente.
- **DRY**: Extraer a componentes/hooks solo cuando hay duplicación real.
- **YAGNI**: No implementar autenticación real hasta que el backend la tenga.

### Convención de Commits (Conventional Commits)
```bash
feat: agregar pantalla de procesamiento de ventas
fix: corregir validación de descuento en formulario
refactor: extraer componente de tabla de productos
test: agregar pruebas para hook useBuscarProductos
style: aplicar formato con Prettier
chore: actualizar dependencias de Vite
docs: documentar estructura de carpetas del frontend
```

### Checklist Pre-Commit
Antes de hacer commit, verificar:
- [ ] `npm run lint` sin errores
- [ ] `npm run build` compila correctamente
- [ ] `npm run test` todas las pruebas pasan
- [ ] No hay `console.log` de debug
- [ ] No hay código comentado innecesario
- [ ] Los tipos TypeScript reflejan exactamente los esquemas Pydantic del backend

---

## 🚫 Reglas Prohibidas

- ❌ Trabajar directamente sobre `main`.
- ❌ Usar `any` en TypeScript.
- ❌ Inventar endpoints que no existen en el backend.
- ❌ Poner lógica de negocio en componentes presentacionales.
- ❌ Hacer llamadas HTTP directamente desde componentes (usar hooks/servicios).
- ❌ Manejar errores HTTP con `try/catch` dispersos (usar interceptor global).
- ❌ Implementar autenticación real sin que el backend la soporte.
- ❌ Instalar librerías sin justificación (YAGNI).
- ❌ Commits con mensajes como "cambios", "arreglos", "update".

---

## 🎯 Objetivo
Construir un frontend **mantenible, tipado, testeable y perfectamente alineado con el backend**, aplicando los principios de Clean Architecture adaptados a React, y evitando alucinaciones del agente de IA mediante reglas estrictas de validación contra la API existente.
```
