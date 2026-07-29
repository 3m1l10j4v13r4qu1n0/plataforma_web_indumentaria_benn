# HU-06: Modelos de Datos (Consultar stock disponible)

## Entidades Involucradas

Esta HU se apoya exclusivamente en la entidad global `Producto`, optimizando su consulta.

### 1. Producto

- `id` (UUID/Int): Identificador único.
- `codigo` (String): Código de barras o SKU. **(Indexado para búsqueda rápida)**
- `nombre` (String): Nombre descriptivo del producto. **(Indexado con búsqueda tipo LIKE o Full-Text)**
- `categoria_id` (Int): Clave foranea autoincremental por ser un catálogo interno de bajo volumen, sin necesidad de UUID.
- `precio` (Int): Nombre descriptivo del precio del producto.
- `stock_actual` (Int): Cantidad disponible en inventario en tiempo real.
- `estado` (Enum): 'ACTIVO' | 'INACTIVO'.

## Reglas de Integridad y Base de Datos

- Se debe crear un índice compuesto o índices individuales en las columnas `codigo` y `nombre` para garantizar que la búsqueda sea rápida (menos de 200ms), ya que se usará frecuentemente en el piso de venta.
- La consulta solo debe devolver productos con `estado = 'ACTIVO'`.

### 2. Categoria

- `id` (Int, autoincremental): Identificador único. Catálogo interno de bajo volumen, no requiere UUID.
- `nombre` (String): Nombre descriptivo de la categoría. **(Único, indexado)**

## Reglas de Integridad y Base de Datos — Categoria

- `nombre` debe tener una restricción `UNIQUE` para evitar categorías duplicadas.
- `Producto.categoria_id` debe tener una `ForeignKey` hacia `Categoria.id`, con `nullable=False` (todo producto pertenece a una categoría).
