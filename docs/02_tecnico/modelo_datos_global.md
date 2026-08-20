# Reglas de Negocio Transversales
Estas reglas aplican a múltiples Historias de Usuario y deben ser respetadas por Backend y Frontend:

1. **Regla de Stock (HU-1, HU-8)**: Ninguna venta puede confirmarse si el `stock_actual` es 0 o menor a la cantidad solicitada. El descuento de stock debe ser automático e inmediato tras la confirmación.
2. **Regla de Plazo de Cambios (HU-2)**: Los cambios de productos solo se permiten dentro de los **15 días calendario** posteriores a la fecha de compra.
3. **Regla de Estado del Producto (HU-3)**: Para aceptar un cambio, el producto debe estar **sin uso** y conservar su **etiqueta** original.
4. **Regla de Comprobante (HU-4)**: Es **obligatorio** presentar el ticket de compra (número de comprobante válido en el sistema) para procesar cualquier cambio.
5. **Regla de Descuentos (HU-5)**: Los descuentos tienen un límite porcentual definido. Cualquier descuento que supere este límite requiere la autorización explícita de un usuario con rol de **Gerente**, quedando registrado en el sistema quién autorizó.
