# HU-02: Requerimientos de Interfaz (Frontend)

## Reglas de Visualización
- Al buscar un ticket, mostrar claramente la **Fecha de Compra** y los **Días Transcurridos**.
- Usar códigos de color para el estado de elegibilidad:
  - 🟢 **Verde**: `dias_transcurridos <= 15` (Cambio permitido).
  - 🔴 **Rojo**: `dias_transcurridos > 15` (Cambio no permitido).

## Estados de la Interfaz y Manejo de Errores
- **Botón "Procesar Cambio"**: Debe estar `disabled` (deshabilitado) por defecto hasta que se cargue un ticket válido y sea elegible (<= 15 días).
- **Manejo de Errores de API (403 Forbidden)**: Si por algún motivo el frontend permite el envío pero el backend rechaza por plazo vencido, mostrar un modal de error no dismissible (que requiera aceptar) con el mensaje: *"El plazo de 15 días para realizar cambios ha expirado para este ticket"*.
