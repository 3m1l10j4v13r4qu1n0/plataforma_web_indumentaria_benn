# HU-06: Especificación de API (Consultar stock disponible)

## Endpoint 1: Búsqueda de Productos y Stock
- **Método**: `GET`
- **Ruta**: `/api/v1/productos/buscar?query={termino}`
- **Descripción**: Busca productos por nombre o código y devuelve su stock actual en tiempo real.
- **Parámetros de Query**:
  - `query` (String, requerido): Término de búsqueda (mínimo 3 caracteres).
- **Respuesta Éxito (200 OK)**:
  ```json
  {
    "resultados": [
      {
        "producto_id": "123",
        "codigo": "CAM-AZU-001",
        "nombre": "Camiseta Azul Talla M",
        "stock_actual": 15,
        "estado": "ACTIVO"
      }
    ],
    "total_encontrados": 1
  }

  ```
- **Respuesta Éxito (200 OK) - Sin resultados**:
  ```json
  {
    "resultados": [],
    "total_encontrados": 0,
    "mensaje": "No se encontraron productos que coincidan con la búsqueda."
  }

  ```
- *Respuesta Error (400 Bad Request)**: Si el parámetro query tiene menos de 3 caracteres.


