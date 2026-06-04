# HU-07: Requerimientos de Interfaz (Frontend)

## Reglas de Visualización
- La pantalla de confirmación de venta debe destacar el **Número de Ticket** y el **Total a Pagar** en tipografía grande y clara.
- Debe incluir un botón prominente de "Reimprimir Ticket" en la pantalla de éxito.

## Estados de la Interfaz y Manejo de Errores
- **Estado de Carga**: Bloquear el botón de "Finalizar Venta" mientras se procesa la petición para evitar ventas duplicadas (doble clic).
- **Manejo de Error de Impresión**: La falla de la impresora **NO** debe revertir ni cancelar la venta registrada. Debe manejarse como una advertencia (UI Toast o Modal) que permita al cajero reintentar la impresión sin perder los datos de la transacción.
- **Formato de Impresión**: El frontend debe generar un formato limpio y legible para impresoras térmicas de 58mm o 80mm (sin logos pesados que consuman tinta/papel innecesariamente).
