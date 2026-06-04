# HU-08: Especificación de Lógica de Servicio (Actualización Automática)

*Nota: Esta HU no expone un endpoint directo al usuario, sino que define la lógica interna que se dispara desde los endpoints de Venta (HU-01) y Devolución (HU-02/03).*

## Servicio: `StockService.actualizarStock(producto_id, cantidad, tipo_movimiento, referencia_id)`
- **Descripción**: Método interno reutilizable que gestiona la modificación del inventario.
- **Lógica**:
  1. Iniciar transacción de base de datos.
  2. Si `tipo_movimiento` == 'VENTA': Restar `cantidad` a `stock_actual`. Validar que no quede en negativo.
  3. Si `tipo_movimiento` == 'DEVOLUCION': Sumar `cantidad` a `stock_actual`.
  4. Insertar registro en la tabla `Movimiento_Stock` para auditoría.
  5. Confirmar transacción (Commit).
- **Manejo de Errores**: Si ocurre cualquier error (ej. constraint de stock negativo), realizar Rollback y lanzar excepción `StockUpdateException`.
