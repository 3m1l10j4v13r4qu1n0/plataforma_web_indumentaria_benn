# HU-02: Caso de Uso Expandido (Interfaz de Cambios)

**Actor Principal**: Cajero
**Precondición**: El cajero ha iniciado sesión y está en la pantalla de "Gestión de Cambios/Devoluciones".

## Flujo Principal (Cambio dentro del plazo)
1. El cajero ingresa o escanea el número de ticket de la compra original.
2. El sistema consulta la venta y calcula los días transcurridos desde la fecha de compra.
3. El sistema muestra los datos de la compra y un indicador visual de que el cambio **está permitido** (ej. "Días transcurridos: 10/15").
4. El cajero selecciona el producto a cambiar y el nuevo producto de reemplazo.
5. El cajero hace clic en "Procesar Cambio".
6. El sistema valida nuevamente en el backend, registra el cambio y muestra un mensaje de "Cambio registrado exitosamente".

## Flujo Alternativo 1: Plazo de 15 días vencido (Rechazo)
1. El cajero ingresa o escanea el número de ticket.
2. El sistema consulta la venta y calcula que han pasado más de 15 días (ej. 20 días).
3. El sistema muestra una alerta prominente en rojo: *"Plazo vencido: Los cambios solo se aceptan hasta 15 días después de la compra"*.
4. El sistema deshabilita el botón "Procesar Cambio" y bloquea la selección de nuevos productos.

## Postcondición
- El estado de la venta original se actualiza (si aplica).
- Se genera un nuevo comprobante o registro del cambio (vinculado a las políticas de la empresa)
