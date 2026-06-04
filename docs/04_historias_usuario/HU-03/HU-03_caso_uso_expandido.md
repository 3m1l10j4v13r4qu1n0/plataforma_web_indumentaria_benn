# HU-03: Caso de Uso Expandido (Interfaz de Validación de Estado)

**Actor Principal**: Cajero / Vendedor
**Precondición**: El cajero ya validó el ticket y el plazo de 15 días (HU-02 y HU-04), y tiene el producto físico en sus manos para inspección.

## Flujo Principal (Producto en buenas condiciones)
1. El sistema muestra la pantalla de "Inspección de Producto" con los datos del producto a cambiar.
2. El cajero inspecciona físicamente el producto (verifica etiqueta, empaque, señales de uso).
3. El cajero selecciona en el sistema: "Producto con etiqueta" (checkbox) y estado "Nuevo/Etiquetado" (dropdown).
4. El cajero puede agregar observaciones opcionales (ej. "Empaque ligeramente abierto pero producto intacto").
5. El cajero hace clic en "Validar Producto".
6. El sistema valida y muestra un indicador verde: ✅ *"Producto apto para cambio"*.
7. El sistema habilita el botón "Continuar con el Cambio" para seleccionar el producto de reemplazo.

## Flujo Alternativo 1: Producto sin etiqueta o con uso (Rechazo)
1. (Pasos 1-2 del flujo principal).
2. El cajero detecta que el producto no tiene etiqueta o presenta señales de uso.
3. El cajero selecciona: "Sin etiqueta" (checkbox desmarcado) o estado "Usado"/"Dañado".
4. El cajero hace clic en "Validar Producto".
5. El sistema muestra una alerta roja: ⚠️ *"Producto no apto para cambio: [motivo específico]"*.
6. El sistema bloquea el flujo y muestra el botón "Cancelar Cambio".
7. El cajero informa al cliente que el cambio no es posible por política de la empresa.

## Postcondición
- Si el producto es apto, se registra la validación en la base de datos y el flujo continúa.
- Si el producto no es apto, se registra el intento de cambio rechazado (para métricas/auditoría).
