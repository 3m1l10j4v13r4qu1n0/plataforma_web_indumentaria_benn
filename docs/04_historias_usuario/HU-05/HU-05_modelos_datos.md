# HU-05: Modelos de Datos (Controlar descuentos)

## Entidades Involucradas
Basado en el modelo global, esta HU impacta las siguientes entidades:

### 1. Venta / Detalle_Venta
- `descuento_porcentaje` (Decimal): Porcentaje de descuento aplicado a la venta o ítem (ej. 10.5).
- `descuento_autorizado_por_id` (UUID/Int, Nullable): FK a la tabla `Usuario`. Solo se llena si el descuento superó el límite permitido y requirió autorización.
- `fecha_autorizacion` (Datetime, Nullable): Momento exacto en que el gerente autorizó el descuento.

### 2. Configuracion_Sistema (Opcional, para flexibilidad)
- `clave` (String): ej. 'LIMITE_DESCUENTO_VENDEDOR'.
- `valor` (Decimal): ej. 20.0 (representa el 20%).

## Reglas de Integridad y Base de Datos
- El campo `descuento_porcentaje` debe ser >= 0.
- Si `descuento_porcentaje` > `LIMITE_DESCUENTO_VENDEDOR`, entonces `descuento_autorizado_por_id` **NO PUEDE SER NULO** (Constraint de base de datos o validación estricta en la capa de servicio).
- El usuario que autoriza debe tener el rol 'GERENTE'.
