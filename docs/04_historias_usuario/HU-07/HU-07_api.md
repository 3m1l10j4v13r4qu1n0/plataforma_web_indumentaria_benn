# HU-07: Especificación de API (Generar ticket de venta)

## Endpoint 1: Finalizar Venta y Generar Ticket
- **Método**: `POST`
- **Ruta**: `/api/v1/ventas`
- **Descripción**: Registra la venta en el sistema y genera el número de ticket único. (Compartido con HU-01, pero aquí se enfatiza la respuesta del ticket).
- **Respuesta Éxito (201 Created)**:
  ```json
  {
    "venta_id": "V-999",
    "numero_ticket": "T-20260604-001",
    "fecha_hora": "2026-06-04T15:30:00Z",
    "total": 45.50,
    "items": [
      { "nombre": "Camiseta Azul", "cantidad": 1, "precio": 25.00 },
      { "nombre": "Calcetines", "cantidad": 2, "precio": 10.25 }
    ],
    "mensaje": "Venta registrada y ticket generado exitosamente."
  }

  ```
## Endpoint 2: Reimprimir Ticket (Opcional)

- **Método**: `GET`
- **Ruta**: `/api/v1/ventas/{venta_id}/ticket`
- **Descripción**: Obtiene los datos formateados del ticket para una reimresión o consulta posterior.
- **Respuesta Éxito (200 OK)**: Devuelve el mismo payload de éxito del Endpoint 1.
