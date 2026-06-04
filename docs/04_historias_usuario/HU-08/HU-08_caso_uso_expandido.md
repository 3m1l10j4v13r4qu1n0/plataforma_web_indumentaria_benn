# HU-08: Caso de Uso Expandido (Feedback de Actualización de Inventario)

**Actor Principal**: Encargado de Ventas / Cajero / Vendedor
**Precondición**: Se ha completado exitosamente una operación de Venta o Devolución.

## Flujo Principal (Post-Venta)
1. El vendedor o cajero confirma la venta en el sistema.
2. El sistema procesa la transacción y, en segundo plano, ejecuta la actualización automática del stock.
3. El sistema muestra un mensaje de confirmación de venta que incluye implícitamente la actualización: *"Venta registrada e inventario actualizado"*.

## Flujo Principal (Post-Devolución/Cambio)
1. El cajero aprueba una devolución o cambio de producto.
2. El sistema procesa la operación y suma automáticamente las unidades devueltas al `stock_actual`.
3. El sistema muestra un mensaje: *"Devolución procesada. Stock del producto actualizado"*.

## Postcondición
- Cualquier consulta de stock (HU-01, HU-06) reflejará inmediatamente el nuevo valor sin necesidad de recargar manualmente el sistema.
