# HU-04: Requerimientos de Interfaz (Frontend)

## Reglas de Visualización
- El campo de búsqueda de ticket debe ser el **primer campo visible y enfocado** (autofocus) al ingresar a la pantalla de cambios.
- Debe permitir tanto entrada manual como escaneo de código de barras (mediante lector USB o cámara).
- Al encontrar un ticket válido, mostrar una tarjeta resumen con:
  - Número de ticket en negrita.
  - Fecha de compra formateada (ej. "20 de Mayo, 2026 - 14:30").
  - Lista de productos comprados (nombre, cantidad, precio).

## Estados de la Interfaz y Manejo de Errores
- **Estado de Carga**: Mientras se consulta la API, mostrar un spinner sobre el botón "Validar Ticket" y deshabilitar el campo de búsqueda para evitar dobles envíos.
- **Manejo de Errores de API (404 Not Found)**: 
  - Mostrar el mensaje de error en un banner rojo persistente en la parte superior de la pantalla.
  - El campo de entrada debe parpadear brevemente en rojo y limpiarse automáticamente después de 3 segundos para facilitar un nuevo intento.
- **Validación de Formato (Frontend)**: Si el formato del ticket es siempre "T-XXXXXXXX-XXX", el frontend debe validar el patrón (regex) antes de enviar la petición a la API para ahorrar viajes innecesarios.
