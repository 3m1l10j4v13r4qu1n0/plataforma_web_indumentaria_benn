# HU-01: Requerimientos de Interfaz (Frontend)

## Reglas de Visualización
- Cada producto agregado al carrito de venta debe mostrar una etiqueta (badge) con el stock:
  - 🟢 **Verde**: `stock_actual > 0`
  - 🔴 **Rojo**: `stock_actual == 0`
- El campo de input "Cantidad a vender" debe tener un atributo `max` dinámico igual al `stock_actual` disponible (validación en el navegador).

## Estados de la Interfaz y Manejo de Errores
- **Botón "Confirmar Venta"**: Debe estar `disabled` (deshabilitado) si la lista contiene al menos un producto con `stock_actual == 0` o si la cantidad solicitada supera el stock.
- **Manejo de Errores de API (409 Conflict)**: Si la API devuelve un error de stock insuficiente (ej. por una condición de carrera donde otro vendedor compró el último producto milisegundos antes), mostrar un toast/notificación persistente: *"El stock de este producto acaba de agotarse. Por favor, retírelo de la venta."* y actualizar la lista automáticamente.
