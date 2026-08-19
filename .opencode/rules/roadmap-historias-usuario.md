# Roadmap y Flujo de Trabajo — SGVIR

## Flujo de generación
NO generar todo el código de una vez. Seguir este orden y esperar confirmación explícita del usuario ("Continuar") entre cada paso:

1. **Paso 1:** Estructura base ([`requirements.txt`](/src/backend/requirements.txt), [`main.py`](/src/backend/app/main.py), [`app/infrastructure/database/session.py`](/src/backend/app/infrastructure/database/session.py), [`app/infrastructure/core/config.py`](/src/backend/app/infrastructure/core/config.py)).
2. **Paso 2:** Modelos SQLAlchemy (`app/domian/models/`) y esquemas Pydantic (`app/presentation/schemas/`) para las entidades globales: `Usuario`, `Producto`, `Venta`, `DetalleVenta`, `Cambio`, `MovimientoStock`.
3. **Paso 3:** [HU-01 (Validar stock antes de vender)](/docs/04_historias_usuario/HU-01/HU-01-validad_stock_anters_de_vender.md). Incluye Router, Service (validación + descuento atómico) y 3 tests Pytest (TDD).
4. **Paso 4:** [HU-05 (Control de descuentos con autorización de gerente)](/docs/04_historias_usuario/HU-05/HU-05-Controlar_descuentos.md).
5. **Paso 5:** Flujo de Cambios ([HU-04](/docs/04_historias_usuario/HU-04/HU-04-Solicitar_ticket_de_compra.md) + [HU-02](docs/04_historias_usuario/HU-02/HU-02-Registrar_cambios_de_productos.md) + [HU-03](/docs/04_historias_usuario/HU-03/HU-03-Validar_estado_del_producto.md)) como servicio unificado.
6. **Paso 6:** [HU-06 (Consulta de stock)](/docs/04_historias_usuario/HU-06/HU-06-Consultar_stock_disponible.md) y [HU-07 (Generación de ticket)](/docs/04_historias_usuario/HU-07/HU-07-Generar_ticket_de_venta.md).
7. **Paso 7:** [HU-08 (Actualización automática de stock en servicios de venta y devolución)](/docs/04_historias_usuario/HU-08/HU-08-Actualizar_stock_automáticamente.md).


> Nota: este archivo es un plan de referencia, no una regla de comportamiento fija. A medida que avance el proyecto, actualizar el estado de cada paso/HU (pendiente / en progreso / hecho).
