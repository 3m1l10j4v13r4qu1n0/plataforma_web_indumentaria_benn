# HU-04: Caso de Uso Expandido (Interfaz de Validación de Ticket)

**Actor Principal**: Cajero
**Precondición**: El cajero está en la pantalla de "Gestión de Cambios/Devoluciones" y el cliente se presenta con un comprobante físico.

## Flujo Principal (Ticket válido)
1. El cajero solicita al cliente el ticket de compra.
2. El cajero ingresa manualmente o escanea el código de barras del `numero_ticket` en el campo de búsqueda.
3. El cajero hace clic en "Validar Ticket".
4. El sistema consulta la API y encuentra el ticket en la base de datos.
5. El sistema muestra un indicador verde ✅ y desglosa los productos comprados en ese ticket.
6. El sistema habilita los siguientes pasos del flujo (selección de producto a cambiar, validación de plazo de 15 días - HU-02, etc.).

## Flujo Alternativo 1: Ticket inexistente o mal ingresado
1. El cajero ingresa un número de ticket que no existe (o con un error de tipeo).
2. El cajero hace clic en "Validar Ticket".
3. El sistema consulta la API y no encuentra coincidencias.
4. El sistema muestra una alerta roja ⚠️: *"El número de ticket ingresado no existe en el sistema. Verifique el comprobante."*
5. El sistema bloquea cualquier avance en el flujo de cambio y limpia el campo de búsqueda para un nuevo intento.

## Flujo Alternativo 2: Cliente sin ticket
1. El cliente indica que no tiene el ticket de compra.
2. El cajero intenta buscar por otros medios (ej. número de tarjeta de crédito - fuera del alcance de esta HU).
3. Al no poder validar un ticket, el cajero hace clic en "Cancelar Cambio".
4. El sistema muestra un mensaje al cliente: *"Por política de la empresa, es obligatorio presentar el ticket de compra para realizar cambios."*

## Postcondición
- Si el ticket es válido, el sistema retiene los datos de la compra en memoria para los siguientes pasos del flujo.
