# HU-01: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Venta con stock disponible (Caso Positivo)
- **Dado** que el producto "Camiseta" tiene un `stock_actual` de 5.
- **Cuando** el vendedor intenta vender 2 unidades de "Camiseta" y confirma la operación.
- **Entonces** el sistema debe aprobar la venta.
- **Y** el `stock_actual` de "Camiseta" debe actualizarse a 3 inmediatamente.

## Escenario 2: Venta con stock en cero (Caso Negativo)
- **Dado** que el producto "Pantalón" tiene un `stock_actual` de 0.
- **Cuando** el vendedor intenta agregar o vender 1 unidad de "Pantalón".
- **Entonces** el sistema debe rechazar la acción.
- **Y** debe mostrar el mensaje de error: "No se puede vender: Producto sin stock disponible".
- **Y** el botón de confirmar venta debe permanecer deshabilitado.

## Escenario 3: Validación de cantidad mayor al stock (Caso Borde)
- **Dado** que el producto "Zapatos" tiene un `stock_actual` de 2.
- **Cuando** el vendedor intenta vender 3 unidades.
- **Entonces** el sistema debe impedir la confirmación.
- **Y** debe mostrar una advertencia indicando que solo hay 2 unidades disponibles.

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_validar_venta_con_stock_suficiente()`
- [ ] `test_rechazar_venta_con_stock_en_cero()`
- [ ] `test_verificar_actualizacion_automatica_del_stock_post_venta()`
