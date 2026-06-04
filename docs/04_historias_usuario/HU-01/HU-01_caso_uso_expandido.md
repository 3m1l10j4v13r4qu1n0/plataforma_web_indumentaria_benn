# HU-01: Caso de Uso Expandido (Interfaz de Venta)

**Actor Principal**: Vendedor
**Precondición**: El vendedor ha iniciado sesión y está en la pantalla de "Nueva Venta".

## Flujo Principal (Éxito)
1. El vendedor escanea o busca un producto por código o nombre.
2. El sistema consulta y muestra el producto en la lista de la venta actual, incluyendo un indicador visual del `stock_actual`.
3. El vendedor ajusta la cantidad a vender (ej. 1 unidad).
4. El vendedor hace clic en el botón "Confirmar Venta".
5. El sistema valida en el backend que la cantidad solicitada sea <= `stock_actual`.
6. El sistema procesa la venta, muestra un mensaje de "Venta Exitosa" y limpia la pantalla para la siguiente operación.

## Flujo Alternativo 1: Stock en Cero (Rechazo en UI)
1. (Pasos 1-3 del flujo principal).
2. El vendedor hace clic en "Confirmar Venta".
3. El sistema detecta que `stock_actual` es 0 (o menor a la cantidad solicitada).
4. El sistema **bloquea** el procesamiento y muestra una alerta modal: *"No se puede vender: El producto [Nombre] no tiene stock disponible"*.
5. El sistema resalta en rojo el producto en la lista y deshabilita el botón "Confirmar Venta" hasta que el producto sea eliminado de la lista.

## Postcondición
- El inventario se refleja actualizado inmediatamente (ver HU-08).
- Se genera el comprobante de venta (ver HU-07).
