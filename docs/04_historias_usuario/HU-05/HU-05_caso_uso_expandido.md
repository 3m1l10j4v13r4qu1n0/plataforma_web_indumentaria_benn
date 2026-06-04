# HU-05: Caso de Uso Expandido (Interfaz de Descuentos)

**Actores Principales**: Vendedor y Gerente
**Precondición**: El vendedor está en la pantalla de "Nueva Venta" con productos agregados.

## Flujo Principal (Descuento dentro del límite)
1. El vendedor ingresa un porcentaje de descuento (ej. 10%) en el campo correspondiente.
2. El vendedor hace clic en "Aplicar Descuento".
3. El sistema valida que el porcentaje sea <= al límite permitido (ej. 20%).
4. El sistema aplica el descuento, actualiza el total a pagar y muestra un mensaje de éxito.

## Flujo Alternativo 1: Descuento alto requiere autorización
1. El vendedor ingresa un porcentaje alto (ej. 40%) y hace clic en "Aplicar Descuento".
2. El sistema detecta que supera el límite y bloquea la aplicación directa.
3. El sistema muestra un modal: *"Este descuento requiere autorización de un Gerente"*.
4. El modal solicita las credenciales (usuario/contraseña o PIN) del Gerente.
5. El Gerente ingresa sus credenciales y el sistema las valida.
6. Si son correctas, el sistema aplica el descuento, actualiza el total y registra internamente que el Gerente X autorizó la operación.

## Postcondición
- El total de la venta refleja el descuento.
- El registro de la venta guarda el ID del gerente autorizador (si aplicó).
