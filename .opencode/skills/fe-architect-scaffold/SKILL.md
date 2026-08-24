---
name: fe-architect-scaffold
description: Estandarizar la implementación del frontend en React.js + Vite + TypeScript, garantizando arquitectura escalable, bajo acoplamiento con la UI y alineación estricta con el backend existente (FastAPI + Clean Architecture). Usar cuando el usuario pida crear una pantalla, componente, hook, servicio o funcionalidad nueva en el frontend, o conectar el frontend a un endpoint del backend.
disable-model-invocation: true
---

# FE Architect Scaffold

Este skill actúa como un **contrato de no-alucinación**: el agente NO puede inventar endpoints, tipos ni comportamientos que no estén documentados en el backend real del SGVIR.

## 📜 Reglas inquebrantables del frontend

### 1. Fuente única de verdad: el backend
- Prohibido inventar endpoints: solo se pueden consumir los documentados en la tabla oficial más abajo.
- Prohibido inventar campos en las respuestas: los tipos TypeScript deben reflejar **exactamente** los esquemas Pydantic del backend.
- Prohibido inventar códigos de error: solo se manejan los que el backend devuelve vía `handlers.py`.

### 2. Separación de responsabilidades
- **Componentes presentacionales (UI)**: solo reciben props y renderizan. No hacen llamadas HTTP ni manejan estado global.
- **Componentes contenedores (Pages/Containers)**: orquestan datos, llaman a servicios/API y pasan props a los presentacionales.
- **Custom Hooks**: encapsulan lógica reutilizable (llamadas HTTP, estado local complejo).
- **Servicios/API Client**: única capa que conoce los endpoints y formatos del backend.

### 3. Manejo centralizado de errores HTTP
- Prohibido usar `try/catch` dispersos en componentes para errores de API.
- Todos los errores HTTP (400, 403, 404, 409, 500) se manejan en un **interceptor global de Axios** o un **ErrorBoundary** de React.
- Los errores de negocio del backend (ej. `STOCK_INSUFICIENTE`, `PLAZO_DE_CAMBIO_VENCIDO`) se mapean a mensajes amigables para el usuario.

### 4. Tipado estricto con TypeScript
- `tsconfig.json` con `"strict": true`.
- Prohibido usar `any`. Si un tipo no está claro, definirlo explícitamente.
- Los tipos de respuesta de API viven en `src/types/api/` y reflejan los esquemas Pydantic.

### 5. Estructura de carpetas estricta

```
src/
├── api/
│   ├── client.ts           # Instancia de Axios con interceptores
│   ├── endpoints.ts        # Constantes de URLs (evita strings mágicos)
│   └── services/
│       ├── venta.service.ts
│       ├── producto.service.ts
│       └── cambio.service.ts
├── components/
│   ├── ui/                 # Botones, inputs, modales, cards
│   └── layout/              # Header, Footer, Sidebar
├── pages/
│   ├── ventas/
│   ├── productos/
│   └── cambios/
├── hooks/                   # useVentas, useProductos, etc.
├── contexts/                # AuthContext, ThemeContext
├── routes/
│   ├── AppRouter.tsx
│   └── ProtectedRoute.tsx   # Preparado para autenticación futura
├── types/
│   ├── api/                 # Espejo de los esquemas Pydantic
│   └── domain/
├── utils/
├── constants/
├── styles/
└── App.tsx
```

### 6. Estado global (YAGNI)
- No usar Redux a menos que sea estrictamente necesario.
- Estado global simple: Context API + `useReducer`.
- Estado global complejo futuro: considerar Zustand.
- Datos de API: TanStack Query (React Query) para cache, refetch y estados de carga/error.

### 7. Preparación para autenticación (fase futura)
- Crear un `AuthContext` vacío con estructura básica (user, token, login, logout).
- Crear un `ProtectedRoute` que redirija a `/login` si no hay token.
- Configurar el interceptor de Axios para inyectar `Authorization: Bearer <token>` cuando exista.
- **NO implementar login real todavía** (YAGNI): solo dejar la estructura lista.

## 🔄 Flujo de trabajo estándar (6 pasos)

Seguir este orden y **esperar confirmación explícita antes de avanzar al siguiente paso**.

### Paso 1: Definición de Tipos y Contratos (API Layer)
**Ubicación**: `src/types/api/` y `src/api/services/`
- Crear los tipos TypeScript que reflejen los esquemas Pydantic del backend (Request y Response).
- Crear la función del servicio que consumirá el endpoint correspondiente.
- **Validación**: comparar línea por línea con el esquema Pydantic del backend. Si hay discrepancia, DETENER y consultar.

### Paso 2: Configuración de Rutas
**Ubicación**: `src/routes/`
- Agregar la nueva ruta en `AppRouter.tsx`.
- Si requiere autenticación (futuro), envolverla en `ProtectedRoute`.
- Definir la ruta en `endpoints.ts` si es un path del frontend.

### Paso 3: Componentes Presentacionales (UI)
**Ubicación**: `src/components/ui/`
- Crear los componentes visuales reutilizables (botones, formularios, tablas, cards).
- Deben recibir solo props tipadas, sin lógica de negocio.
- Aplicar estilos consistentes (Tailwind o CSS Modules).

### Paso 4: Custom Hooks (Lógica de UI)
**Ubicación**: `src/hooks/`
- Crear hooks como `useVentas`, `useProductos`, `useBuscarProductos`.
- El hook encapsula: estado de carga, estado de error, datos, y la llamada al servicio.
- Si se usa TanStack Query, el hook envuelve `useQuery` o `useMutation`.

### Paso 5: Página/Contenedor (Orquestación)
**Ubicación**: `src/pages/`
- Crear la página que consume el hook y renderiza los componentes presentacionales.
- Manejar los tres estados universales: Loading, Error, Success.
- NO hacer llamadas HTTP directamente acá; delegar al hook.

### Paso 6: Pruebas de Componentes
**Ubicación**: `src/__tests__/` o junto al componente (`*.test.tsx`)
- Usar Vitest + React Testing Library.
- Probar comportamiento, no implementación (ej. "al hacer clic se muestra el modal", no "se llama a setState").
- Mockear los servicios API con `vi.mock()`.

## 📋 Lista oficial de endpoints del backend (anti-alucinación)

⚠️ **Regla de oro**: solo se pueden consumir estos endpoints. Si necesitás uno que no está acá, DETENÉ la implementación y consultá al usuario.

> ⚠️ **Mantenimiento**: esta tabla debe actualizarse en el mismo commit que agrega un endpoint nuevo al backend (ver `di-architect-scaffold/SKILL.md`, sección Documentación). Si sospechás que está desactualizada, verificar contra el router real (`app/presentation/routers/`) antes de asumir que un endpoint no existe.

| Método | Endpoint | Propósito | HU asociada |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/ventas` | Procesar venta (valida stock, descuentos) | HU-01, HU-05, HU-07, HU-08 |
| `GET` | `/api/v1/productos/{codigo}/stock` | Consultar stock de un producto | HU-01 |
| `GET` | `/api/v1/productos/buscar?query=...` | Buscar productos por nombre/código | HU-06 |
| `GET` | `/api/v1/ventas/validar-ticket/{numero_ticket}` | Validar existencia de ticket y obtener datos de la compra | HU-04 |
| `PATCH` | `/api/v1/ventas/{numero_ticket}/estado` | Marcar venta como EN_CAMBIO (retiene el ticket) | HU-04 |
| `POST` | `/api/v1/cambios` | Registrar cambio de producto (valida plazo 15 días) | HU-02 |
| `POST` | `/api/v1/cambios/{cambio_id}/validar-estado` | Validar estado físico del producto presentado a cambio | HU-03 |

> Nota: el health check real del backend es `GET /` (no existe `/health`).

### Estructura de respuestas de error del backend

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

### Códigos HTTP y su significado

| Código | Significado | Acción en frontend |
| :--- | :--- | :--- |
| `200` | Éxito (GET, PUT) | Mostrar datos |
| `201` | Creado (POST) | Mostrar confirmación + redirigir si aplica |
| `400` | Error de validación / regla de negocio | Mostrar mensaje al usuario |
| `403` | No autorizado (ej. descuento sin gerente) | Mostrar mensaje específico |
| `404` | Recurso no encontrado | Mostrar "No encontrado" |
| `409` | Conflicto (ej. stock insuficiente) | Mostrar conflicto y ofrecer alternativa |
| `500` | Error interno del servidor | Mostrar "Error inesperado, contacte soporte" |

## 🛠️ Stack tecnológico recomendado

| Categoría | Tecnología | Justificación |
| :--- | :--- | :--- |
| Build Tool | Vite | Rápido, moderno, configuración mínima |
| Framework | React 18+ | Estándar de la industria |
| Lenguaje | TypeScript (strict) | Tipado fuerte, evita bugs |
| Router | React Router v6 | Estándar para SPA |
| HTTP Client | Axios | Interceptores, fácil manejo de errores |
| Estado API | TanStack Query (opcional) | Cache, refetch, estados de carga |
| Estado Global | Context API + useReducer | Simple, sin dependencias extra |
| Estilos | Tailwind CSS | Rápido, consistente, utility-first |
| Testing | Vitest + React Testing Library | Rápido, alineado con Vite |
| Linting | ESLint + Prettier | Calidad de código |
| Formularios | React Hook Form + Zod | Validación tipada en el borde |

## 🌱 Cultura de Desarrollo

### Principios
- **Clean Code**: nombres descriptivos, componentes pequeños (<150 líneas).
- **SOLID**: SRP en componentes, DIP en servicios.
- **KISS**: no sobre-ingenierizar. Si un `div` basta, no crear un componente.
- **DRY**: extraer a componentes/hooks solo cuando hay duplicación real.
- **YAGNI**: no implementar autenticación real hasta que el backend la tenga.

### Convención de commits

**Usar la convención definida en [`AGENTS.md`] del proyecto** (español, prefijo + descripción breve). No usar Conventional Commits en inglés salvo indicación explícita.

### Checklist pre-commit

- [ ] `npm run lint` sin errores
- [ ] `npm run build` compila correctamente
- [ ] `npm run test` — todas las pruebas pasan
- [ ] No hay `console.log` de debug
- [ ] No hay código comentado innecesario
- [ ] Los tipos TypeScript reflejan exactamente los esquemas Pydantic del backend

## 📋 Lista de verificación anti-alucinación

Antes de generar código, verificar:

- [ ] ¿El endpoint que voy a consumir existe en la tabla oficial de arriba?
- [ ] ¿Los tipos TypeScript reflejan exactamente los esquemas Pydantic del backend?
- [ ] ¿Los códigos de error HTTP que voy a manejar están documentados en `handlers.py` del backend?
- [ ] ¿Estoy respetando la estructura de carpetas definida?
- [ ] ¿Estoy usando `any` en TypeScript? → Si es sí, DETENER y corregir.
- [ ] ¿Estoy poniendo lógica de negocio en un componente presentacional? → Si es sí, DETENER y mover a hook.
- [ ] ¿Estoy implementando autenticación real? → Si es sí, DETENER: el backend aún no la tiene.

Si detectás que se necesita un endpoint que **no existe** en el backend, **DETENÉ la implementación y notificá antes de continuar.**

## 🚫 Reglas prohibidas

- Trabajar directamente sobre `main`.
- Usar `any` en TypeScript.
- Inventar endpoints que no existen en el backend.
- Poner lógica de negocio en componentes presentacionales.
- Hacer llamadas HTTP directamente desde componentes (usar hooks/servicios).
- Manejar errores HTTP con `try/catch` dispersos (usar interceptor global).
- Implementar autenticación real sin que el backend la soporte.
- Instalar librerías sin justificación (YAGNI).
- Commits con mensajes vagos ("cambios", "arreglos", "update").

## 🎯 Objetivo

Construir un frontend mantenible, tipado, testeable y perfectamente alineado con el backend, aplicando Clean Architecture adaptada a React, y evitando alucinaciones del agente mediante reglas estrictas de validación contra la API existente.