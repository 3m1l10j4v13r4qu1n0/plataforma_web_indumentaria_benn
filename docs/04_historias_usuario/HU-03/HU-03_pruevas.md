# HU-03: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Producto nuevo y etiquetado (Caso Positivo)
- **Dado** que un cliente presenta un producto para cambio.
- **Cuando** el cajero valida que el producto tiene su etiqueta y no presenta señales de uso.
- **Entonces** el sistema debe marcar el producto como "Apto para cambio".
- **Y** debe habilitar el flujo para continuar con el cambio.

## Escenario 2: Producto usado (Caso Negativo)
- **Dado** que un cliente presenta un producto que evidencia señales de uso.
- **Cuando** el cajero registra el estado como "Usado".
- **Entonces** el sistema debe rechazar el producto.
- **Y** debe mostrar un mensaje indicando que no se aceptan productos usados.
- **Y** debe bloquear el botón de continuar el cambio.

## Escenario 3: Producto sin etiqueta (Caso Negativo / Borde)
- **Dado** que un cliente presenta un producto nuevo pero sin etiqueta.
- **Cuando** el cajero desmarca el checkbox "Tiene etiqueta".
- **Entonces** el sistema debe rechazar el producto.
- **Y** debe mostrar el motivo específico: "Producto sin etiqueta original".

## Escenario 4: Producto dañado (Caso Negativo / Borde)
- **Dado** que un cliente presenta un producto dañado.
- **Cuando** el cajero registra el estado como "Dañado".
- **Entonces** el sistema debe rechazar el cambio.
- **Y** debe solicitar obligatoriamente observaciones del daño.

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_validar_producto_nuevo_con_etiqueta_es_apto()`
- [ ] `test_rechazar_producto_usado()`
- [ ] `test_rechazar_producto_sin_etiqueta()`
- [ ] `test_rechazar_producto_danado_con_observaciones_obligatorias()`
- [ ] `test_verificar_registro_en_bd_de_validacion_aprobada()`
- [ ] `test_verificar_registro_en_bd_de_validacion_rechazada()`
