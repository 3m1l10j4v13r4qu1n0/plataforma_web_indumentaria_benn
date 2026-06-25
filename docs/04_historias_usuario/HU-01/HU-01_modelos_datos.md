# HU-01: Modelos de Datos (Validar stock antes de vender)

## Entidades Involucradas
Basado en el modelo global, esta HU impacta directamente las siguientes entidades:

### 1. Producto
- `id` (UUID/Int): Identificador único.
- `codigo` (String): Código de barras o SKU (índice de búsqueda).
- `nombre` (String): Nombre descriptivo del producto.
- `categoria` (int): categoria del producto.
- `precio` (int): precio del producto.
- `stock_actual` (Int): Cantidad disponible en inventario. **(Campo crítico)**
- `estado` (Enum): 'ACTIVO' | 'INACTIVO'.

### 2. Venta
- `id` (UUID/Int): Identificador único de la transacción.
- `fecha_hora` (Datetime): Momento de la transacción.
- `vendedor_id` (UUID/Int): ID del usuario que realiza la venta.
- `estado` (Enum): 'PENDIENTE' | 'CONFIRMADA' | 'CANCELADA'.

### 3. Detalle_Venta
- `venta_id` (UUID/Int): FK a Venta.
- `producto_id` (UUID/Int): FK a Producto.
- `cantidad` (Int): Unidades vendidas de este producto.

## Reglas de Integridad y Base de Datos
- El campo `stock_actual` debe tener una restricción a nivel de base de datos para nunca ser negativo (`CHECK stock_actual >= 0`).
- La operación de descuento de stock al confirmar la venta debe ser **atómica (transaccional)** para evitar condiciones de carrera (race conditions) si dos vendedores venden el último producto al mismo tiempo.
