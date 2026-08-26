# Estado del Proyecto — SGVIR

Snapshot vigente de la implementación. **NO asumas estado viejo** ni de memoria ni de sesiones anteriores: este archivo es la fuente rápida de contexto y el código es la fuente definitiva. Si algo de acá contradice el código, gana el código — y actualizá este archivo en el mismo commit para no volver a desincronizar.

Última sincronización: 2026-08-26.

## Historias de Usuario

| HU | Módulo | Backend | Frontend |
|----|--------|:-------:|:--------:|
| HU-01 Validar stock antes de vender | Ventas | ✅ | ✅ |
| HU-02 Registrar cambios (plazo 15 días) | Cambios | ✅ | ✅ |
| HU-03 Validar estado del producto | Cambios | ✅ | ✅ |
| HU-04 Solicitar ticket de compra | Cambios | ✅ | ✅ |
| HU-05 Controlar descuentos (autorización gerente) | Admin | ✅ | ✅ (modal) |
| HU-06 Consultar stock disponible | Ventas | ✅ | ✅ |
| HU-07 Generar ticket de venta | Ventas | ✅ | ✅ |
| HU-08 Actualizar stock automáticamente | Inventario | ✅ | ✅ (feedback post-venta) |

## Endpoints vivos (fuente: `app/presentation/routers/`)

Todos con prefijo `/api/v1`:

| Método | Ruta | HU |
|--------|------|----|
| GET | `/productos/{codigo}/stock` | HU-06 |
| GET | `/productos/buscar?query=` | HU-06 |
| POST | `/ventas` | HU-01 / HU-07 |
| GET | `/ventas/validar-ticket/{numero_ticket}` | HU-04 |
| PATCH | `/ventas/{numero_ticket}/estado` | HU-04 |
| POST | `/cambios` | HU-02 |
| POST | `/cambios/{cambio_id}/validar-estado` | HU-03 |
| POST | `/descuentos` | HU-05 |
| GET | `/dashboard/resumen` | Dashboard |
| GET | `/dashboard/productos-stock-bajo` | Dashboard |

Health check: `GET /` → `{"estado": "ok", ...}`. **NO existe `/health`.**

Códigos HTTP de error de negocio: `404` no encontrado · `409` conflictos de stock/ticket duplicado/venta ya en cambio · `422` validaciones de negocio · `403` plazo vencido.

## Pantallas frontend (fuente: `src/routes/AppRouter.tsx`)

- `/dashboard` — Panel principal con métricas del día + accesos rápidos + stock bajo
- `/productos/stock` — Consulta de stock con badges 3 niveles (HU-06)
- `/ventas` — Nueva venta con carrito tabular + modal de descuentos (HU-01 / HU-07 / HU-05)
- `/cambios` — Wizard de cambios e inspección de producto (HU-04 / HU-02 / HU-03)
- `/registro` — Alta de usuarios (solo GERENTE)
- `/login` — Inicio de sesión
- Cualquier otra ruta cae en 404

## Verificación conocida en verde

- Backend: `ruff check .`, `black --check .`, `pytest` (55 tests, fakes en memoria, sin DB)
- Frontend: `npm run lint` (oxlint), `npm run build`, `npm run test` (37 tests)

## Deuda / pendientes conocidos

- `GET /api/v1/productos/{producto_id}/validaciones` (historial de inspecciones, HU-03): **opcional**, no implementado.
- Roles/RBAC completo: fuera de alcance. Solo se valida rol GERENTE para `/registro` a nivel de ruta.
