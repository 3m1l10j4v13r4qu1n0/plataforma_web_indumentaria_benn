# HU-06: Caso de Uso Expandido (Interfaz de Consulta de Stock)

**Actor Principal**: Vendedor
**Precondición**: El vendedor está en el piso de venta, atendiendo a un cliente, y necesita verificar la disponibilidad de un artículo.

## Flujo Principal (Producto encontrado)
1. El vendedor accede a la pantalla o módulo de "Consultar Stock".
2. El vendedor ingresa el nombre o escanea el código del producto en la barra de búsqueda.
3. El sistema realiza la búsqueda en tiempo real (con un pequeño debounce de 300ms).
4. El sistema muestra una lista con los productos coincidentes, destacando el nombre, código y, muy visiblemente, la **cantidad de stock disponible**.
5. El vendedor informa al cliente sobre la disponibilidad.

## Flujo Alternativo 1: Producto inexistente o sin coincidencias
1. El vendedor ingresa un término de búsqueda.
2. El sistema no encuentra ningún producto activo que coincida.
3. El sistema muestra un mensaje claro en el centro de la pantalla: *"No se encontraron productos que coincidan con '[término]'."*
4. El sistema sugiere verificar el código o el nombre.

## Postcondición
- El vendedor obtiene la información necesaria en segundos, sin necesidad de desplazarse al depósito.
