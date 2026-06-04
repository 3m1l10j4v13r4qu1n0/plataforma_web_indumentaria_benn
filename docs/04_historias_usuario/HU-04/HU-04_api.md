# HU-04: Especificación de API (Solicitar ticket de compra)

## Endpoint 1: Validar Existencia de Ticket
- **Método**: `GET`
- **Ruta**: `/api/v1/ventas/validar-ticket/{numero_ticket}`
- **Descripción**: Verifica si un ticket existe en el sistema y devuelve los datos de la compra para iniciar el flujo de cambio.
- **Respuesta Éxito (200 OK)**:
  ```json
  {
    "existe": true,
    "numero_ticket": "T-20260601-001",
    "fecha_compra": "2026-05-20T14:30:00Z",
    "cajero_original_id": "C-003",
    "items": [
      { "producto_id": "123", "nombre": "Camiseta Azul", "cantidad": 1, "precio": 25.00 }
    ],
    "mensaje": "Ticket válido. Puede continuar con el proceso de cambio."
  }

  ```

- **Respuesta Error (404 Not Found)**:
  ```json
  {
    "existe": false,
    "error": "TICKET_NO_ENCONTRADO",
    "mensaje": "El número de ticket ingresado no existe en el sistema. Verifique el comprobante."
  }

  ```

## Endpoint 2: Marcar Ticket como "En Proceso de Cambio" (Opcional)

- **Método**: `PATCH`
- **Ruta**: `/api/v1/ventas/{numero_ticket}/estado`
- **Descripción**: Cambia el estado de la venta a 'EN_CAMBIO' para evitar que dos cajeros procesen el mismo ticket simultáneamente en diferentes cajas.


---

