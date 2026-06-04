# HU-04: Modelos de Datos (Solicitar ticket de compra)

## Entidades Involucradas
Esta HU se apoya en la entidad `Venta` (ya definida globalmente) y la extiende para el flujo de cambios.

### 1. Venta (Consulta y Validación)
- `numero_ticket` (String): Identificador único alfanumérico del comprobante (ej. "T-20260601-001"). **(Campo crítico para la búsqueda)**
- `fecha_hora` (Datetime): Fecha y hora de la compra original.
- `estado` (Enum): 'CONFIRMADA' | 'CAMBIADA_PARCIALMENTE' | 'DEVUELTA_TOTAL'.
- `items` (Array): Lista de productos vendidos con su `producto_id`, `cantidad` y `precio_unitario`.

### 2. Cambio (Extensión de HU-02)
- `ticket_referencia` (String): FK lógica al `numero_ticket` de la venta original.
- `validado_por_cajero_id` (UUID/Int): Cajero que validó la existencia del ticket.

## Reglas de Integridad y Base de Datos
- El campo `numero_ticket` debe ser **único** (UNIQUE constraint) en la tabla `Venta`.
- El índice de búsqueda de `numero_ticket` debe estar optimizado para consultas rápidas (B-Tree index).
- No se puede registrar un `Cambio` si el `ticket_referencia` no existe en la tabla `Venta` (Foreign Key lógica validada en servicio).
