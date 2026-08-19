# Reglas de Negocio Críticas — SGVIR

Estas reglas son de cumplimiento obligatorio en toda la lógica de negocio (`app/domain/services/`). NO deben ignorarse ni relajarse al generar código, aunque no se mencionen explícitamente en una tarea puntual.

1. **Stock nunca negativo:** El `stock_actual` de un producto NUNCA puede quedar en un valor negativo. Las operaciones de venta y devolución que afecten stock deben ejecutarse como transacciones atómicas (ACID).

2. **Cambios de producto (HU-02, HU-03, HU-04):** Solo se permite registrar un cambio si se cumplen TODAS estas condiciones:
   - a) Existe el ticket original de compra.
   - b) Han pasado 15 días o menos desde la fecha de compra.
   - c) El producto está en estado "NUEVO" y "CON ETIQUETA" (sin uso, sin daños).

3. **Descuentos (HU-05):** Existe un porcentaje máximo permitido (ej. 20%) sin autorización especial. Si el descuento solicitado supera ese límite, el sistema DEBE exigir y registrar el `gerente_id` que autorizó la operación. No se permite aplicar un descuento alto sin esa autorización registrada.

4. **Tickets (HU-07):** El `numero_ticket` debe ser único en el sistema y generarse automáticamente al momento de confirmar la venta (nunca ingresado manualmente por el usuario).
