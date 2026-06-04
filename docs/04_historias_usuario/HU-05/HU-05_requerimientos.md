# HU-05: Requerimientos de Interfaz (Frontend)

## Reglas de Visualización
- El campo de "Porcentaje de Descuento" debe ser un input numérico con un placeholder que indique el límite máximo sin autorización (ej. "Máx. 20% sin autorización").
- Mostrar el monto total descontado y el nuevo total a pagar en tiempo real (mientras sea válido).

## Estados de la Interfaz y Manejo de Errores
- **Modal de Autorización**: Debe ser un componente seguro (ej. input de tipo password para el PIN del gerente) que no guarde la contraseña en el historial del navegador.
- **Manejo de Errores de API**: 
  - Si el gerente ingresa credenciales incorrectas, mostrar: *"Credenciales de gerente inválidas"*.
  - Si la API retorna `403 Forbidden`, mostrar el modal de autorización.
