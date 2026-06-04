# HU-08: Requerimientos de Interfaz (Frontend)

## Reglas de Visualización
- No se requiere una pantalla específica para esta HU, ya que es un comportamiento del sistema.
- Sin embargo, las pantallas de Venta (HU-01) y Cambios (HU-02) deben mostrar un indicador de carga (spinner) mientras se procesa la transacción completa (incluyendo la actualización de stock).

## Estados de la Interfaz
- **Éxito**: Mostrar notificación tipo "Toast" verde: *"Operación exitosa. Inventario actualizado"*.
- **Error de Concurrencia**: Si el backend rechaza la operación porque el stock cambió en el último milisegundo, mostrar: *"El stock del producto cambió recientemente. Por favor, verifique la cantidad disponible"*.
