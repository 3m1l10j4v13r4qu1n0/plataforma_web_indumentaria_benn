# HU-06: Requerimientos de Interfaz (Frontend)

## Reglas de Visualización
- La barra de búsqueda debe tener un ícono de "escáner de código de barras" para facilitar el uso con pistolas lectoras USB.
- Los resultados deben mostrarse en formato de tarjetas o lista compacta.
- El `stock_actual` debe mostrarse con un badge de color:
  - 🟢 **Verde**: `stock_actual > 5`
  - 🟡 **Amarillo**: `1 <= stock_actual <= 5` (Stock bajo)
  - 🔴 **Rojo**: `stock_actual == 0` (Agotado)

## Estados de la Interfaz y Manejo de Errores
- **Debounce**: La búsqueda no debe dispararse con cada tecla, sino esperar 300ms después de que el usuario deje de escribir, para no sobrecargar la API.
- **Estado de Carga**: Mostrar un spinner sutil dentro del campo de búsqueda o junto al botón mientras se consultan los datos.
- **Manejo de Errores**: Si la API falla (ej. error 500), mostrar un toast: *"Error de conexión. No se pudo consultar el stock en este momento."*
