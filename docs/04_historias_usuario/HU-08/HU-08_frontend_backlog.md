# HU-08: Backlog Frontend (Feedback de Actualización de Inventario)

> **Estado**: PENDIENTE — se posterga para próximas iteraciones del proyecto.
> El backend de HU-08 está completo y publicado con el tag
> `hu-08-actualizacion-automatica-stock-v1.0.0` (rama `feature/HU-08-refactor`,
> fusionada a `develop`). Este documento resume lo que falta del lado del
> frontend y cómo implementarlo cuando se retome.

## Contexto

La actualización de stock es un comportamiento interno del sistema: el backend
descuenta/incrementa stock y registra auditoría de forma atómica al confirmar
una venta (y en el futuro, una devolución). Por eso esta HU **no requiere
pantallas nuevas ni endpoints nuevos**: todo el trabajo pendiente es de
*feedback* al usuario dentro de las pantallas ya existentes.

Fuente de verdad de los requisitos:
- `HU-08_requerimientos.md` (estados de la interfaz y mensajes)
- `HU-08_caso_uso_expandido.md` (flujos post-venta y post-devolución)

## Tareas pendientes

### 1. Mapear los códigos de error nuevos (`apiErrors.ts`)

El backend expone dos códigos nuevos que el frontend debe traducir a mensajes
amigables en `src/utils/apiErrors.ts` (`MENSAJES_AMIGABLES`):

```typescript
ERROR_ACTUALIZACION_STOCK:
  'El stock del producto cambió recientemente. Por favor, verifique la cantidad disponible.',
CANTIDAD_MOVIMIENTO_INVALIDA:
  'La cantidad indicada no es válida para actualizar el inventario.',
```

- `ERROR_ACTUALIZACION_STOCK` (HTTP 409): error de concurrencia definido en
  `HU-08_requerimientos.md`; usar el mensaje textual exigido por la doc.
- `CANTIDAD_MOVIMIENTO_INVALIDA` (HTTP 422): validación defensiva del caso de
  uso de stock.

### 2. Confirmación de éxito tipo Toast

Requisito textual (`HU-08_requerimientos.md`):
> **Éxito**: Mostrar notificación tipo "Toast" verde: *"Operación exitosa.
> Inventario actualizado"*.

Y el mensaje post-venta según `HU-08_caso_uso_expandido.md`:
> *"Venta registrada e inventario actualizado"*.

**Dónde**: `CrearVentaPage.tsx`, al dispararse `onSuccess` de `ventaMutation`.

**Opciones de implementación** (decidir al retomar):

| Opción | Pros | Contras |
| :--- | :--- | :--- |
| Componente `Toast` casero (portal + auto-dismiss) | Sin dependencias nuevas; cumple la doc al pie de la letra | ~60 líneas de código + test propio |
| Reutilizar `Alert variant="success"` inline | Cero código nuevo; ya existe | No es un toast flotante como pide la doc |

Nota: hoy NO hay ninguna librería de toasts en `package.json`
(sonner/react-hot-toast). Si se prefiere librería, evaluarla en esa iteración.

### 3. Spinner durante la transacción completa

Estado actual: el botón muestra texto `"Procesando..."` vía
`ventaMutation.isPending`. La doc pide un indicador de carga (spinner) visible
mientras se procesa la transacción completa (incluida la actualización de stock).

**Sugerencia**: spinner pequeño dentro del botón (patrón habitual) o overlay en
la tarjeta "Resumen de venta". Es mejora cosmética, prioridad baja.

### 4. Feedback post-devolución

> *"Devolución procesada. Stock del producto actualizado"*

**Bloqueado**: depende del flujo de Cambios/Devoluciones (HU-02/03/04), que
todavía no tiene pantalla propia en el frontend. Implementar junto con esa HU.

## Checklist de pruebas (cuando se implemente)

- [ ] Venta exitosa muestra la notificación verde con el texto requerido.
- [ ] Error `ERROR_ACTUALIZACION_STOCK` (409) muestra el mensaje de concurrencia exacto.
- [ ] Botón/deshabilitación correcta mientras `isPending` (spinner).
- [ ] Tras cerrar la notificación, una nueva búsqueda refleja el stock actualizado.
- [ ] Tests unitarios de `CrearVentaPage` actualizados (mockear respuestas 409).

## Referencias técnicas (backend ya implementado)

| Pieza | Ubicación |
| :--- | :--- |
| Caso de uso transaccional | `app/application/use_cases/actualizar_stock_use_case.py` |
| Auditoría en flujo de venta | `validar_stock_venta_use_case.py` (registra movimiento por ítem) |
| Handlers HTTP de los errores | `app/presentation/handlers.py` (409 / 422) |
| Tabla de auditoría | `movimientos_stock` (CHECK constraints de tipo y signo) |
