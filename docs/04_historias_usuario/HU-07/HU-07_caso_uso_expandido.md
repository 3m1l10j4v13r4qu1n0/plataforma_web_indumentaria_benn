# HU-07: Caso de Uso Expandido (Interfaz de Generación de Ticket)

**Actor Principal**: Cajero
**Precondición**: El cajero ha escaneado todos los productos y el cliente ha realizado el pago.

## Flujo Principal (Éxito)
1. El cajero hace clic en el botón "Finalizar Venta y Cobrar".
2. El sistema envía la solicitud al backend y muestra un indicador de carga (spinner).
3. El backend registra la venta, genera el número de ticket único y devuelve la confirmación.
4. El sistema muestra una pantalla de éxito con el `numero_ticket` en grande y el monto total.
5. El sistema envía automáticamente la orden de impresión a la impresora térmica (o muestra un preview para imprimir en PDF).
6. El cajero entrega el comprobante físico al cliente.

## Flujo Alternativo 1: Error de impresión
1. (Pasos 1-3 del flujo principal: la venta se registra correctamente en la base de datos).
2. El sistema intenta enviar la orden a la impresora, pero esta está desconectada o sin papel.
3. El sistema detecta el fallo de impresión.
4. El sistema muestra una advertencia clara: *"Venta registrada exitosamente (Ticket: T-XXX), pero hubo un error de impresión. ¿Desea reimprimir?"*
5. El cajero puede solucionar el problema de la impresora y hacer clic en "Reimprimir" o entregar un comprobante manual si la política lo permite.

## Postcondición
- La venta queda registrada en el sistema (cumpliendo con la necesidad de mantener registro de operaciones).
- El cliente recibe su comprobante, habilitando futuros cambios (HU-04).
