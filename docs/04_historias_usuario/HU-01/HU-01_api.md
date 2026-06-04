# HU-01: Especificación de API (Validar stock antes de vender)

## Endpoint 1: Consultar Stock (Para UI en tiempo real)
- **Método**: `GET`
- **Ruta**: `/api/v1/productos/{codigo}/stock`
- **Descripción**: Obtiene el stock actual de un producto específico para mostrarlo al vendedor antes de agregarlo al carrito.
- **Respuesta Éxito (200 OK)**:
  ```json
  {
    "producto_id": "123",
    "nombre": "Camiseta Básica",
    "stock_actual": 5
  }
  
  ```
- **Respuesta Error (404 Not Found)**: Producto no existe en el sistema.

## Endpoint 2: Procesar Venta (Validación y Descuento)
- **Método**:`POST`
- **Ruta**: `/api/v1/ventas`
- **Descripción**: Valida el stock de todos los items en el payload. Si es válido, confirma la venta y descuenta el inventario en una sola transacción.
- **Request Body**:

```json
{
  "vendedor_id": "V-001",
  "items": [
    { "producto_id": "123", "cantidad": 2 }
  ]
}
```

- **Respuesta Éxito (201 Created)**: Venta registrada y stock descontado correctamente.
- **Respuesta Error (409 Conflict)**:

```json
{
  "error": "STOCK_INSUFICIENTE",
  "mensaje": "El producto 'Camiseta Básica' no tiene stock disponible para la cantidad solicitada.",
  "producto_id": "123"
}

```

---


