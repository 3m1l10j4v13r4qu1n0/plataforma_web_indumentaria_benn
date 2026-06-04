# HU-08: Modelos de Datos (Actualizar stock automáticamente)

## Entidades Involucradas
Esta HU define el comportamiento transaccional de las entidades existentes:

### 1. Producto
- `stock_actual` (Int): Debe actualizarse de forma atómica.

### 2. Movimiento_Stock (Entidad de Auditoría - Recomendada)
Registra el historial de por qué cambió el stock.
- `id` (UUID/Int): Identificador único del movimiento.
- `producto_id` (UUID/Int): FK a Producto.
- `tipo_movimiento` (Enum): 'VENTA' | 'DEVOLUCION' | 'AJUSTE'.
- `cantidad` (Int): Cantidad modificada (negativa para ventas, positiva para devoluciones).
- `fecha_hora` (Datetime): Momento del cambio.
- `documento_referencia_id` (UUID/Int): ID de la Venta o del Cambio/Devolución que originó el movimiento.

## Reglas de Integridad y Base de Datos
- Las operaciones que modifican `stock_actual` (ventas y devoluciones) deben ejecutarse dentro de una **transacción de base de datos (ACID)**.
- Si falla la creación del registro en `Movimiento_Stock`, se debe hacer rollback de la venta/devolución para mantener la consistencia.
