# 🏛️ Resumen de la Arquitectura Frontend Implementada

## 1. Visión y Alcance

Se ha construido la capa de presentación del sistema retail SGVIR, proporcionando una interfaz web responsiva que consume la API REST del backend (FastAPI + Clean Architecture). El frontend garantiza validaciones en el borde, feedback visual inmediato al usuario y una experiencia ágil para los actores principales (Vendedor y Cajero), manteniendo una alineación estricta con los contratos del backend mediante un **contrato de no-alucinación**.

---

## 2. Patrón Arquitectónico: Clean Architecture Adaptada a React

El frontend se estructura en capas concéntricas con dependencias que fluyen desde afuera (UI) hacia adentro (tipos de dominio), siguiendo el patrón **Presentación → Contenedores → Hooks → Servicios → Tipos**.

| Capa | Ubicación | Responsabilidad | Dependencias |
|---|---|---|---|
| **Presentación (UI)** | `src/components/ui/`, `src/components/layout/` | Componentes puros que solo reciben props y renderizan | Solo utilidades (`cn`, `formatCurrency`) |
| **Contenedores (Pages)** | `src/pages/` | Orquestan hooks y componentes, manejan los 4 estados universales | Hooks + componentes UI |
| **Lógica de UI (Hooks)** | `src/hooks/` | Encapsulan llamadas HTTP, estado local y TanStack Query | Servicios API + tipos |
| **Servicios API** | `src/api/services/` | Única capa que conoce endpoints y formatos del backend | Cliente Axios + tipos |
| **Tipos** | `src/types/` | Tipos TypeScript espejo de esquemas Pydantic | Ninguna (capa más interna) |

### Flujo de Datos

```
Usuario → Componente UI → Contenedor (Page) → Custom Hook → Servicio API → Backend
         ↑                ↑                   ↑               ↑
         props            estado              TanStack        Axios +
         (puro)           universal           Query cache     interceptores
```

---

## 3. Reglas Inquebrantables Aplicadas (SGVIR Frontend)

Durante todo el desarrollo, se respetaron rigurosamente las siguientes reglas:

### 🚫 Contrato de No-Alucinación
- **Prohibido inventar endpoints**: Solo se consumen los 6 endpoints documentados en `FE-Architect-Scaffold.md`.
- **Prohibido inventar campos**: Los tipos TypeScript reflejan exactamente los esquemas Pydantic del backend (snake_case → camelCase mediante mappers).
- **Prohibido inventar códigos de error**: Solo se manejan los errores que el backend devuelve vía `handlers.py` (`STOCK_INSUFICIENTE`, `PLAZO_DE_CAMBIO_VENCIDO`, `TICKET_NO_ENCONTRADO`, etc.).

### 🧱 Separación de Responsabilidades Estricta
- **Componentes UI**: Cero lógica de negocio, cero llamadas HTTP, cero estado global.
- **Contenedores**: Solo orquestan, no renderizan lógica compleja.
- **Hooks**: Encapsulan estado + llamadas HTTP, exponen interfaces limpias.
- **Servicios**: Única capa que conoce URLs y formatos del backend.

### 🛡️ Manejo Centralizado de Errores
- **Interceptor global de Axios**: Captura todos los errores HTTP (4xx, 5xx) y los traduce a `ApiErrorResponse`.
- **ErrorBoundary de React**: Captura errores de renderizado (crashes de React).
- **Cero `try/catch` dispersos** en componentes o hooks para errores de API.

### 📝 Tipado Estricto
- `tsconfig.json` con `"strict": true` y `"noImplicitAny": true`.
- **Prohibido `any`** en todo el código.
- Mappers explícitos (`toStockProducto`, `toItemCarrito`, `toVentaProcesada`, `toTicket`, `toElegibilidadCambio`) para conversión snake_case ↔ camelCase.

---

## 4. Decisiones de Diseño Destacadas (SOLID, KISS, DRY, YAGNI)

### SRP con Componentes Atómicos
Cada componente tiene una única responsabilidad clara:
- `StockBadge` → Solo muestra nivel de stock
- `QuantityInput` → Solo maneja input numérico con controles +/−
- `CartItemRow` → Solo renderiza una fila del carrito
- `ReceiptTicket` → Solo presenta el ticket con formato térmico

### DIP con Servicios Abstraídos
Los contenedores dependen de hooks (`useCart`, `useProcessSale`), no de Axios directamente. Esto permite:
- Mockear fácilmente en tests con `vi.mock()`
- Cambiar el cliente HTTP sin tocar la UI
- Probar comportamiento, no implementación

### KISS/YAGNI en Decisiones Críticas
- **Sin autenticación real**: `AuthContext` vacío + `ProtectedRoute` preparado (YAGNI hasta que el backend lo soporte).
- **Sin Redux**: Context API + TanStack Query son suficientes.
- **Sin impresión real**: `usePrinter` simula con `setTimeout` (1.5s).
- **Sin ruta independiente para el ticket**: Se reutiliza `/ventas/nueva` con vista condicional.
- **Sin `SaleSuccessModal`**: Reemplazado por `SaleTicketView` más completo (HU-07).

### DRY con Utilidades Centralizadas
- `cn()` → Combinación segura de clases Tailwind (clsx + tailwind-merge).
- `formatCurrency()` → Formateo consistente de montos en ARS.
- `formatRelativeTime()` → Fechas relativas en español (date-fns).
- `productosQueryKeys` / `productSearchQueryKeys` → Claves de cache centralizadas.

### Mapper Pattern para Aislamiento de Dominio
Los tipos de API (snake_case, espejo de Pydantic) se convierten a tipos de dominio (camelCase, ergonómicos para React) mediante mappers puros:
```ts
toStockProducto(item: ProductoBusquedaItem): StockProducto
toItemCarrito(stock: StockResponse, cantidad?: number): ItemCarrito
toVentaProcesada(response: VentaResponse): VentaProcesada
toTicket(params: {...}): Ticket
toElegibilidadCambio(response: ElegibilidadCambioResponse): ElegibilidadCambio
```

### Estados Universales en Contenedores
Cada página maneja consistentemente los 4 estados:
- **Idle** → Estado inicial (ej: carrito vacío, búsqueda sin ejecutar)
- **Loading** → Primera carga (spinner)
- **Error** → Fallo HTTP (alerta con mensaje del backend)
- **Success** → Datos disponibles (renderizado normal)
- **Empty** → Búsqueda exitosa pero sin resultados (caso especial)

---

## 5. Historias de Usuario Implementadas (Frontend)

| HU | Módulo | Descripción | Estado Frontend | Artefactos Clave |
|---|---|---|---|---|
| **HU-01** | Ventas | Validar stock antes de vender | ✅ Completada | `NuevaVentaPage`, `useCart`, `useProcessSale`, `useCartValidation` |
| **HU-06** | Consultas | Consultar stock disponible | ✅ Completada | `ConsultarStockPage`, `useBuscarProductos`, `StockResultCard` |
| **HU-07** | Ventas | Generar ticket de venta | ✅ Completada | `SaleTicketView`, `ReceiptTicket`, `usePrinter` |
| **HU-08** | Inventario | Actualizar stock automáticamente | ✅ Completada (sin UI) | Invalidación de cache en `useProcessSale` |
| **HU-04** | Cambios | Solicitar ticket de compra | 🚧 En progreso | `GestionCambiosPage`, `TicketSearchInput`, `PlazoIndicator` |
| **HU-02** | Cambios | Registrar cambios (15 días) | ⏳ Pendiente | — |
| **HU-03** | Cambios | Validar estado del producto | ⏳ Pendiente | — |
| **HU-05** | Admin | Controlar descuentos | ⏳ Pendiente | — |

### Flujo de Implementación (6 Pasos por HU)
Cada HU se implementa siguiendo estrictamente:
1. **Tipos y Contratos** → Espejo de Pydantic + mappers
2. **Configuración de Rutas** → Registro en `AppRouter.tsx`
3. **Componentes Presentacionales** → UI pura en `src/components/ui/`
4. **Custom Hooks** → Lógica de UI en `src/hooks/`
5. **Página/Contenedor** → Orquestación en `src/pages/`
6. **Pruebas de Componentes** → Vitest + React Testing Library

---

## 6. Estrategia de Testing (TDD + Behavior-Driven)

### Stack de Testing
- **Vitest** → Runner rápido, alineado con Vite
- **React Testing Library** → Pruebas basadas en comportamiento del usuario
- **user-event** → Simulación realista de interacciones
- **vi.mock()** → Aislamiento de servicios HTTP
- **Fake Timers** → Control de `setTimeout` en hooks asíncronos

### Cobertura por Unidad
| Unidad | Qué se prueba | Dónde |
|---|---|---|
| **Mappers** | Conversión snake_case → camelCase | `src/types/__tests__/` |
| **Hooks** | Estado local, llamadas HTTP, invalidación de cache | `src/hooks/__tests__/` |
| **Contenedores** | 4 estados universales + flujo completo | `src/pages/**/__tests__/` |
| **Componentes clave** | Renderizado condicional (solo los de alto ROI) | `src/components/**/__tests__/` |

### Principios de Testing
- ✅ **Probar comportamiento, no implementación** (ej: "al presionar Enter se agrega al carrito", no "se llama a setState").
- ✅ **Mockear servicios con `vi.mock()`** para aislar unidades.
- ✅ **Cubrir los 4 estados universales** en cada contenedor.
- ✅ **No sobre-testear**: Componentes UI pequeños no se prueban (over-testing).
- ✅ **Fake Timers** para controlar delays simulados (ej: `usePrinter`).

### Utilidades Compartidas
- `test-utils.tsx` → Wrapper con `QueryClientProvider` + `BrowserRouter` para tests.
- `createTestQueryClient()` → Cliente fresco por test, sin reintentos.
- `renderWithProviders()` → Custom render con todos los contextos inyectados.

---

## 7. Stack Tecnológico Definitivo

| Categoría | Tecnología | Versión | Justificación |
|---|---|---|---|
| Build Tool | **Vite** | 5.x | Rápido, HMR instantáneo |
| Framework | **React** | 18.x | Estándar de la industria |
| Lenguaje | **TypeScript** | 5.x (strict) | Tipado fuerte, cero `any` |
| Router | **React Router** | v6 | SPA estándar |
| HTTP Client | **Axios** | 1.x | Interceptores globales |
| Estado API | **TanStack Query** | 5.x | Cache, refetch, deduplicación |
| Estado Global | **Context API** | — | Simple, sin dependencias |
| Estilos | **Tailwind CSS** | 3.x | Utility-first, consistente |
| Testing | **Vitest + RTL** | — | Rápido, alineado con Vite |
| Formularios | **React Hook Form + Zod** | — | Validación tipada en el borde |
| Utilidades | **clsx + tailwind-merge** | — | Combinación segura de clases |
| Fechas | **date-fns** | — | Formateo ligero y modular |

---

## 8. Integración con el Backend

### Alineación de Contratos
El frontend actúa como un **cliente estricto** del backend:
- Los tipos `src/types/api/*.types.ts` son **espejo exacto** de los esquemas Pydantic (`venta_schema.py`, `producto_schema.py`, `ticket_schema.py`, `cambio_schema.py`).
- Los mappers convierten snake_case (backend) ↔ camelCase (frontend) de forma explícita.
- Los códigos de error (`STOCK_INSUFICIENTE`, `PLAZO_DE_CAMBIO_VENCIDO`, etc.) se mapean a mensajes amigables.

### Endpoints Consumidos
| Método | Endpoint | HU Asociada | Servicio Frontend |
|---|---|---|---|
| POST | `/api/v1/ventas` | HU-01, HU-05, HU-07, HU-08 | `ventaService.procesarVenta()` |
| GET | `/api/v1/productos/buscar?query=...` | HU-06 | `productosService.buscarProductos()` |
| GET | `/api/v1/productos/{codigo}/stock` | HU-01 | `productosService.obtenerStock()` |
| GET | `/api/v1/ventas/tickets/{numero_ticket}` | HU-04 | `cambioService.obtenerDetalleTicket()` |
| POST | `/api/v1/cambios/validar-elegibilidad` | HU-02, HU-03, HU-04 | `cambioService.validarElegibilidad()` |

### Estrategia de Cache
- **TanStack Query** con `staleTime: 30_000` (30 segundos de cache fresco).
- **Invalidación automática** después de `POST /api/v1/ventas` → `queryClient.invalidateQueries({ queryKey: productSearchQueryKeys.all })`.
- **Deduplicación** de peticiones simultáneas al mismo endpoint.

---

## 9. Preparación para Futuro (YAGNI Controlado)

### Autenticación (Fase Futura)
- ✅ `AuthContext` con estructura básica (`user`, `token`, `login`, `logout`).
- ✅ `ProtectedRoute` que redirige a `/login` si no hay token.
- ✅ Interceptor de Axios que inyecta `Authorization: Bearer <token>` cuando existe.
- ❌ **NO se implementa login real** (el backend aún no lo tiene).

### Escalabilidad
- Estructura de carpetas modular por dominio (`ventas/`, `productos/`, `cambios/`).
- Servicios aislados por dominio (fácil agregar nuevos módulos).
- Hooks reutilizables (ej: `useProductSearch` usado en HU-01 y HU-06).
- Componentes UI atómicos (fácil componer nuevas pantallas).

---

## 10. Métricas de Calidad

| Métrica | Estado |
|---|---|
| **Cero `any` en TypeScript** | ✅ Cumplido |
| **Componentes <150 líneas** | ✅ Cumplido |
| **Commits atómicos (Conventional Commits)** | ✅ Cumplido |
| **Cero lógica de negocio en UI pura** | ✅ Cumplido |
| **Cero `try/catch` dispersos** | ✅ Cumplido |
| **Cero endpoints inventados** | ✅ Cumplido |
| **Cobertura de tests en contenedores** | ✅ 4 estados universales probados |
| **Alineación con Pydantic** | ✅ Mappers explícitos |

---

## 📌 Conclusión

El frontend del SGVIR se ha construido siguiendo una **arquitectura limpia, tipada y testeable**, perfectamente alineada con el backend FastAPI. La aplicación de estricta de los principios **SOLID, KISS, DRY y YAGNI**, junto con el **contrato de no-alucinación**, garantiza que el código sea mantenible, escalable y libre de sorpresas.

Las **4 HUs completadas** (HU-01, HU-06, HU-07, HU-08) demuestran que el scaffold de 6 pasos funciona correctamente y puede replicarse para las HUs restantes (HU-02, HU-03, HU-04, HU-05) manteniendo la misma calidad y consistencia.

---

*Documento generado para fines académicos. Última actualización: Junio 2026.*