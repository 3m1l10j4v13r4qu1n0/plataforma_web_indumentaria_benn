# HU-02: Especificación de API (Registrar cambios de productos)

## Endpoint 1: Consultar Venta por Ticket (Validación previa)
- **Método**: `GET`
- **Ruta**: `/api/v1/ventas/ticket/{numero_ticket}`
- **Descripción**: Obtiene los datos de la venta original para validar si es elegible para cambio.
- **Respuesta Éxito (200 OK)**:
```json
  {
    "numero_ticket": "T-20231015-001",
    "fecha_compra": "2023-10-15T10:30:00Z",
    "dias_transcurridos": 10,
    "es_elegible_para_cambio": true,
    "items": [
      { "producto_id": "123", "nombre": "Camiseta", "cantidad": 1 }
    ]
  }

```

## Endpoint 2: Procesar Cambio de Producto

- **Método**:`POST`
- **Ruta**:`/api/v1/cambios`
- **Descripción**: Registra el cambio de un producto, validando estrictamente que no hayan pasado más de 15 días desde la compra.
- **Request Body**:

```json
{
  "venta_original_id": "V-999",
  "cajero_id": "C-005",
  "producto_a_cambiar_id": "123",
  "nuevo_producto_id": "124"
}

```
- **Respuesta Éxito (201 Created)**: Cambio registrado exitosamente.
- **Respuesta Error (403 Forbidden)**: 

```json
{
  "error": "PLAZO_VENCIDO",
  "mensaje": "El plazo de 15 días para realizar cambios ha expirado para este ticket."
}

```

---

