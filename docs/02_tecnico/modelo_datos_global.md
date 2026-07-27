# Modelo de Datos Global (Entidades Base)

Estas entidades son la base sobre la cual se construyen las HU específicas.

- **Producto**: `id`, `codigo`, `nombre`, `categoria_id`, `precio`, `stock_actual` (int, >=0), `estado` (Activo/Inactivo).
- **Categoria**: `id` (int, autoincremental), `nombre` (string, único). Catálogo interno de bajo volumen, no requiere UUID.
- **Venta**: `id`, `fecha_hora`, `cajero_id`, `vendedor_id`, `total`, `estado` (Confirmada/Cancelada).
- **Detalle_Venta**: `venta_id`, `producto_id`, `cantidad`, `precio_unitario`.
- **Usuario**: `id`, `nombre`, `rol` (Vendedor, Cajero, Gerente, Encargado).
