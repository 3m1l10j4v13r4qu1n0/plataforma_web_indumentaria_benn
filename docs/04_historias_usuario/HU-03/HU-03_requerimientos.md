# HU-03: Requerimientos de Interfaz (Frontend)

## Reglas de Visualización
- La pantalla de inspección debe mostrar una foto o descripción clara del producto esperado para que el cajero pueda comparar.
- El campo "Tiene etiqueta" debe ser un checkbox prominente.
- El dropdown de "Estado del producto" debe tener 3 opciones claramente diferenciadas por color:
  - 🟢 **Nuevo y etiquetado** (Apto)
  - 🟡 **Usado leve** (No apto)
  - 🔴 **Dañado** (No apto)

## Estados de la Interfaz y Manejo de Errores
- **Botón "Validar Producto"**: Debe estar `disabled` hasta que el cajero seleccione obligatoriamente el estado del producto.
- **Validación en tiempo real**: Si el cajero desmarca "Tiene etiqueta" o selecciona "Usado/Dañado", el sistema debe mostrar **inmediatamente** (sin esperar al clic) una advertencia: *"Este producto no será apto para cambio según las políticas de la empresa"*.
- **Campo "Observaciones"**: Si el producto no es apto, el campo de observaciones se vuelve **obligatorio** para registrar el motivo del rechazo.
