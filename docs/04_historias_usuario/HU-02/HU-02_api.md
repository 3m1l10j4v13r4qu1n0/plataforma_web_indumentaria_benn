# HU-02: Especificación de API (Registrar cambios de productos)

## Endpoint 1: Consultar Venta por Ticket (Validación previa)
La validación previa del ticket está definida como parte del flujo de solicitud de ticket (HU-04). Ver su especificación completa (ruta, payload de éxito y error) en [`HU-04_api.md`](../HU-04/HU-04_api.md):
- **Método**: `GET`
- **Ruta**: `/api/v1/ventas/validar-ticket/{numero_ticket}`

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

