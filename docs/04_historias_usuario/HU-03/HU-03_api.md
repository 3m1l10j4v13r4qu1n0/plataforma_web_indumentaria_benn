# HU-03: Especificación de API (Validar estado del producto devuelto)

## Endpoint 1: Registrar Validación de Estado
- **Método**: `POST`
- **Ruta**: `/api/v1/cambios/{cambio_id}/validar-estado`
- **Descripción**: Valida el estado físico del producto que el cliente desea cambiar. Si el producto no cumple las condiciones, rechaza el cambio.
- **Request Body**:
  
  ```json
  {
    "producto_id": "123",
    "estado_producto": "NUEVO_ETIQUETADO",
    "tiene_etiqueta": true,
    "observaciones": "Producto en perfectas condiciones",
    "cajero_id": "C-005"
  }

  ```
- **Respuesta Éxito (200 OK)**:
  
  ```json
  {
    "mensaje": "Producto validado correctamente. Puede continuar con el cambio.",
    "es_apto_para_cambio": true
  }

  ```

- **Respuesta Error (422 Unprocessable Entity)**:

  ```json
  {
    "error": "PRODUCTO_NO_APTO",
    "mensaje": "El producto no cumple las condiciones para ser cambiado.",
    "motivo": "PRODUCTO_USADO_O_SIN_ETIQUETA",
    "es_apto_para_cambio": false
  }

  ```

## Endpoint 2: Consultar Historial de Validaciones (Opcional)

- **Método**: `GET`
- **Ruta**: `/api/v1/productos/{producto_id}/validaciones`
- **Descripción**: Devuelve el historial de validaciones de estado de un producto específico (útil para auditoría).

---
