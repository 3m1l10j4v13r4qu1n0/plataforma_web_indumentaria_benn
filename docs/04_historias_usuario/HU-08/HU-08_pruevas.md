# HU-08: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Descuento de stock por venta (Caso Positivo)
- **Dado** que un producto tiene un `stock_actual` de 10.
- **Cuando** se confirma una venta de 1 unidad de ese producto.
- **Entonces** el sistema debe descontar 1 unidad automáticamente.
- **Y** el `stock_actual` debe ser 9 inmediatamente.
- **Y** debe existir un registro en el historial de movimientos con tipo 'VENTA'.

## Escenario 2: Incremento de stock por devolución (Caso Positivo)
- **Dado** que un producto tiene un `stock_actual` de 5.
- **Cuando** se aprueba una devolución de 2 unidades de ese producto.
- **Entonces** el sistema debe incrementar el stock automáticamente.
- **Y** el `stock_actual` debe ser 7 inmediatamente.
- **Y** debe existir un registro en el historial de movimientos con tipo 'DEVOLUCION'.

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_descuento_automatico_de_stock_al_vender()`
- [ ] `test_incremento_automatico_de_stock_al_devolver()`
- [ ] `test_verificar_creacion_de_registro_en_movimientos_stock()`
- [ ] `test_rollback_de_transaccion_si_falla_la_actualizacion_de_stock()`
