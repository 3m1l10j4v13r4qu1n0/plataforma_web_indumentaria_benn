# HU-06: Modelos de Datos (Consultar stock disponible)

## Entidades Involucradas
Esta HU se apoya exclusivamente en la entidad global `Producto`, optimizando su consulta.

### 1. Producto
- `id` (UUID/Int): Identificador único.
- `codigo` (String): Código de barras o SKU. **(Indexado para búsqueda rápida)**
- `nombre` (String): Nombre descriptivo del producto. **(Indexado con búsqueda tipo LIKE o Full-Text)**
- `stock_actual` (Int): Cantidad disponible en inventario en tiempo real.
- `estado` (Enum): 'ACTIVO' | 'INACTIVO'.

## Reglas de Integridad y Base de Datos
- Se debe crear un índice compuesto o índices individuales en las columnas `codigo` y `nombre` para garantizar que la búsqueda sea rápida (menos de 200ms), ya que se usará frecuentemente en el piso de venta.
- La consulta solo debe devolver productos con `estado = 'ACTIVO'`.
