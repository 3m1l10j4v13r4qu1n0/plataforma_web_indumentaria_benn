# HU-05: Especificación de API (Controlar descuentos)

## Endpoint 1: Solicitar Aplicación de Descuento
- **Método**: `POST`
- **Ruta**: `/api/v1/ventas/{venta_id}/descuento`
- **Descripción**: Intenta aplicar un descuento a una venta en curso. Valida si requiere autorización.
- **Request Body**:
  ```json
  {
    "porcentaje": 40,
    "vendedor_id": "V-001"
  }

  ```
- **Respuesta Éxito (200 OK)**: (Si está dentro del límite, ej. 10%)
  ```json
  { 
    "error": "AUTORIZACION_REQUERIDA", 
    "mensaje": "El descuento supera el límite permitido. Se requiere autorización de un Gerente." 
  }

  ``` 
### Endpoint 2: Autorizar Descuento (Solo Gerentes)

- **Método**: `POST`
- **Ruta**: `/api/v1/descuentos/autorizar`
- **Descripción**: Un gerente aprueba un descuento que estaba pendiente.
- **Request Body**:
  ```jsom
  {
    "venta_id": "V-999",
    "gerente_id": "G-001",
    "porcentaje_autorizado": 40
  }

  ```
- **Respuesta Éxito (200 OK)**: Descuento registrado y venta actualizada.

---

