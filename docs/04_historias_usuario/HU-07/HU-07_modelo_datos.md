# HU-07: Modelos de Datos (Generar ticket de venta)

## Entidades Involucradas
Esta HU consolida la entidad `Venta` y su relación con los detalles, asegurando la trazabilidad del comprobante.

### 1. Venta
- `id` (UUID/Int): Identificador interno único.
- `numero_ticket` (String): Identificador alfanumérico único del comprobante (ej. "T-20260604-001"). **(Campo crítico, UNIQUE constraint)**
- `fecha_hora` (Datetime): Fecha y hora exacta del cierre de la venta.
- `cajero_id` (UUID/Int): FK al usuario que procesó la venta.
- `total` (Decimal): Monto total de la transacción.
- `estado` (Enum): 'CONFIRMADA' | 'CANCELADA'.

### 2. Detalle_Venta
- `venta_id` (UUID/Int): FK a Venta.
- `producto_id` (UUID/Int): FK a Producto.
- `cantidad` (Int): Unidades vendidas.
- `precio_unitario` (Decimal): Precio al momento de la venta (para historial, independientemente de cambios futuros de precio).

## Reglas de Integridad y Base de Datos
- El `numero_ticket` debe generarse de forma automática y secuencial (o mediante UUID corto) al momento de confirmar la venta, garantizando que no haya duplicados.
- La creación de la `Venta` y sus `Detalle_Venta` debe ser una operación atómica (transaccional). Si falla el detalle, no se genera el ticket.
