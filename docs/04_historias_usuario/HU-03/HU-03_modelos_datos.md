# HU-03: Modelos de Datos (Validar estado del producto devuelto)

## Entidades Involucradas
Basado en el modelo global, esta HU extiende la entidad `Cambio` (creada en HU-02):

### 1. Cambio (Extensión)
- `estado_producto` (Enum): 'NUEVO_ETIQUETADO' | 'USADO' | 'DANADO'. **(Campo crítico)**
- `tiene_etiqueta` (Boolean): Indicador de si el producto conserva su etiqueta original.
- `observaciones` (String, Nullable): Comentarios del cajero sobre el estado físico del producto.
- `fecha_validacion` (Datetime): Momento en que se realizó la inspección.
- `cajero_id` (UUID/Int): FK al cajero que realizó la validación física.

## Reglas de Integridad y Base de Datos
- Si `estado_producto` es 'USADO' o 'DANADO', o si `tiene_etiqueta` es `false`, el registro del cambio **NO DEBE PERSISTIRSE** en la base de datos (validación previa en la capa de servicio).
- El campo `estado_producto` es obligatorio al momento de registrar cualquier cambio o devolución.
- Se recomienda crear un constraint CHECK: `CHECK (estado_producto IN ('NUEVO_ETIQUETADO', 'USADO', 'DANADO'))`.
