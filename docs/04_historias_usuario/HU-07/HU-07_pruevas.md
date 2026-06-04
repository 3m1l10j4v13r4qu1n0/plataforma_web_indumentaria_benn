# HU-07: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Venta confirmada genera ticket (Caso Positivo)
- **Dado** que el cajero finaliza una venta con productos en el carrito.
- **Cuando** el sistema procesa la operación exitosamente.
- **Entonces** el sistema debe generar un número de ticket único.
- **Y** debe guardar la fecha, hora y productos vendidos en el registro de la base de datos.

## Escenario 2: Error de impresión post-venta (Caso Borde)
- **Dado** que la venta se registró correctamente en la base de datos.
- **Cuando** el sistema intenta enviar la orden a la impresora y esta falla.
- **Entonces** el sistema debe mostrar una advertencia de error de impresión al cajero.
- **Y** debe ofrecer la opción de "Reimprimir" sin cancelar la venta ya registrada.

## Escenario 3: Validación de unicidad del ticket (Caso Negativo / Borde)
- **Dado** que se realizan dos ventas simultáneas.
- **Cuando** el sistema genera los comprobantes.
- **Entonces** cada venta debe tener un `numero_ticket` completamente único.
- **Y** no debe permitir la duplicidad en la base de datos.

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_generar_ticket_con_datos_correctos()`
- [ ] `test_verificar_datos_registrados_en_detalle_venta()`
- [ ] `test_validar_numero_unico_de_comprobante()`
- [ ] `test_manejo_de_error_de_impresion_sin_revertir_venta()`
