# HU-06: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Producto existente (Caso Positivo)
- **Dado** que existe un producto activo con código "CAM-001" y stock de 10 unidades.
- **Cuando** el vendedor busca por "CAM-001" o "Camiseta".
- **Entonces** el sistema debe mostrar el producto en los resultados.
- **Y** debe mostrar correctamente la cantidad disponible (10).

## Escenario 2: Producto inexistente (Caso Negativo)
- **Dado** que no existe ningún producto con el código "XYZ-999".
- **Cuando** el vendedor realiza la búsqueda con ese término.
- **Entonces** el sistema debe mostrar un mensaje de error o "sin resultados".
- **Y** no debe mostrar datos de productos inactivos o inexistentes.

## Escenario 3: Búsqueda con término muy corto (Caso Borde)
- **Dado** que el vendedor ingresa solo 2 caracteres (ej. "CA").
- **Cuando** intenta realizar la búsqueda.
- **Entonces** el sistema no debe enviar la petición a la API.
- **Y** debe mostrar una validación en el frontend: "Ingrese al menos 3 caracteres".

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_buscar_producto_por_codigo_existente()`
- [ ] `test_buscar_producto_por_nombre_existente()`
- [ ] `test_buscar_producto_inexistente_retorna_lista_vacia()`
- [ ] `test_validar_que_no_se_muestren_productos_inactivos()`
- [ ] `test_verificar_tiempo_de_respuesta_de_la_consulta(< 200ms)`
