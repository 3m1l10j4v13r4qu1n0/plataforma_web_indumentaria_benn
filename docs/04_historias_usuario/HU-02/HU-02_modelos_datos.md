# HU-02: Modelos de Datos (Registrar cambios de productos)

## Entidades Involucradas
Basado en el modelo global, esta HU impacta e introduce las siguientes entidades:

### 1. Venta (Consulta)
- `id` / `numero_ticket` (String/UUID): Identificador único de la venta original.
- `fecha_hora` (Datetime): Fecha y hora exacta de la compra original. **(Campo crítico para el cálculo)**
- `estado` (Enum): 'CONFIRMADA' | 'CAMBIADA' | 'DEVUELTA'.

### 2. Cambio (Nueva Entidad)
Registra la operación de intercambio de productos.
- `id` (UUID/Int): Identificador único del cambio.
- `venta_original_id` (UUID/Int): FK a la Venta original.
- `fecha_cambio` (Datetime): Fecha y hora en que se procesa el cambio.
- `cajero_id` (UUID/Int): ID del usuario que autoriza/procesa el cambio.
- `motivo` (String): Razón del cambio (opcional, pero recomendado).
- `estado` (Enum): 'APROBADO' | 'RECHAZADO_PLAZO'.

## Reglas de Integridad y Base de Datos
- El sistema debe calcular la diferencia en días entre `fecha_hora` (de la Venta) y la fecha actual del sistema.
- Si la diferencia es `> 15` días, la creación del registro en la tabla `Cambio` debe ser rechazada a nivel de lógica de negocio (y preferiblemente con un constraint o trigger de validación si aplica).
