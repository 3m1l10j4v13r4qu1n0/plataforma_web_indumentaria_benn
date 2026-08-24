# Auditoría de Cumplimiento — Mockups (Contrato Visual) vs Frontend Implementado

> **Fecha**: 24/08/2026 · **Rama**: `feat/frontend-mockups-mvp`
> **Alcance**: comparación elemento-por-elemento entre los mockups HTML de
> `docs/05_mockups/` (aprobados por el cliente = **contrato visual**) y el
> frontend React implementado (`src/frontend/`).
>
> **Leyenda de estado**: ✅ cumple · 🟡 parcial / divergente · ❌ no cumple ·
> ⛔ bloqueado (dependencia externa)

## Decisiones registradas

Estas desviaciones respecto al contrato fueron analizadas y aprobadas por el
usuario. Cualquier desviación futura debe agregarse acá antes de implementarse.

| ID | Decisión | Motivo |
| :--- | :--- | :--- |
| D-001 | **Color primario unificado a azul brand.** El contrato usa azul en HU-01/HU-05, índigo en HU-02/03/04 y teal en HU-06/07. Se adopta un único color de marca (familia azul, ya existente como `--color-brand-*`). Los headers teal/índigo del mockup se implementan en azul. | Consistencia de marca; los mockups son internamente inconsistentes. |
| D-002 | **HU-05 mantiene el flujo post-venta real** (endpoint `POST /api/v1/descuentos` con `autorizado_por` + `motivo`), pero la UI se rediseña para parecerse al mockup (header naranja "Autorización Requerida", hint del límite 20%). Los campos del mockup (correo/PIN del gerente) se mapean a `autorizado_por`/`motivo`. | El backend define el flujo transaccional real; el descuento pre-venta del mockup exigiría endpoints nuevos. La estética sí sigue al contrato. |
| D-003 | **HU-02/03/04 sin pantallas**: quedan en backlog hasta que el backend exponga endpoints de cambios/devoluciones (hoy `app/presentation/routers/` solo tiene venta, producto y descuento). Prohibido inventar endpoints (`src/api/endpoints.ts`). | Regla dura del proyecto: no consumir endpoints inexistentes. |
| D-004 | **HU-06 sin "Última actualización"**: el timestamp por producto que muestra el mockup no existe en la API (`ProductoBusquedaResponse` no expone fecha de actualización). Se omite hasta que el backend lo agregue. | Mismo motivo que D-003. |

## 1. Design System global

| Aspecto | Contrato (mockups) | Frontend actual | Estado | Acción |
| :--- | :--- | :--- | :--- | :--- |
| Tipografía base | Google Fonts `Inter` (400/500/600/700) | system-ui default de Tailwind | ❌ | Importar Inter y definirla como `--font-sans` |
| Tipografía mono | `JetBrains Mono` para el ticket (HU-07) | `font-mono` default | 🟡 | Importar JetBrains Mono como `--font-mono` |
| Color primario | Azul / índigo / teal según pantalla | Azul brand unificado | 🟡 | Mantener azul → decisión D-001 |
| Neutros | Escala `gray-*` | Escala `slate-*` | 🟡 | Mantener slate (equivalente visual); estética flexible |
| Éxito / peligro / advertencia | green / red / orange+yellow | emerald / rose / amber | 🟡 | Alinear tokens funcionales a green/red/orange en `@theme` |
| Alerta de error | Patrón `border-l-4` (borde izq. grueso) + fondo `*-50` | Card redondeada estándar | ❌ | Agregar variante `border-l-4` al componente `Alert` |
| Radios | Contenedor `rounded-xl`, componentes `rounded-lg`, badges `rounded-full` | Coincide en general | ✅ | — |
| Sombras | `shadow-lg` página, `shadow-2xl` modal/ticket | `shadow-sm` general | 🟡 | Alinear en pantallas específicas |
| Formato moneda | `$XX.XX` consistente | `$${precio}` sin formato fijo | 🟡 | Helper centralizado `formatoMoneda()` |
| Fechas | Heterogéneas pero todas es-AR | `es-AR` puntual en ticket | 🟡 | Helper centralizado `formatoFecha()` |
| Navegación global | Ninguna pantalla tiene navbar/sidebar | Sin navegación cruzada (solo link en 404) | ✅ | Fuera del contrato; evaluar AppShell en otra iteración |
| Interactividad | Sin JS propio; estados alternativos documentados como comentarios HTML | Estados alternativos no implementados | ❌ | Ver sección 3: cada estado comentado es obligatorio |

## 2. Matriz por pantalla

### HU-01 — Nueva Venta (`mockup_hu01.html`) → `/ventas`

| Elemento | Contrato (texto exacto) | Frontend actual | Estado | Acción |
| :--- | :--- | :--- | :--- | :--- |
| Título página | `Nueva Venta` | `Procesar Venta` | ❌ | Cambiar texto |
| Contexto usuario header | `Cajero: Juan Pérez \| Caja: 01` + fecha | Meta `{label:'Vendedor', value:'V-001'}` hardcodeado | 🟡 | Alinear formato; mantener vendedor configurable |
| Label búsqueda | `Buscar o escanear producto` | Sin label, solo placeholder | ❌ | Agregar label |
| Placeholder búsqueda | `Ej: CAM-001 o 'Camiseta Básica'` | `Buscar producto por código...` | ❌ | Cambiar texto |
| Encabezado sección | `Productos a vender` | Panel derecho `Resumen de venta` | 🟡 | Usar textos del contrato |
| Estructura carrito | Tabla: `Producto · Precio Unit. · Stock Actual · Cantidad · Subtotal` | Lista de filas (`VentaItemRow`) | ❌ | Convertir panel a tabla con columnas exactas |
| Badge stock | `5 disponibles` (verde) / `0 disponibles` (rojo) | `10 en stock` / `agotado` | ❌ | Adoptar formato `N disponibles`; nivel amarillo ver HU-06 |
| Fila sin stock | Fila completa `bg-red-50`, input disabled, subtotal `$0.00` | Botón cambia a `Sin stock` y bloquea input | 🟡 | Resaltar fila entera en rojo |
| Alerta de bloqueo | `No se puede procesar la venta` + `El producto "X" no tiene stock disponible. Por favor, elimínalo del carrito para continuar.` — preventiva, antes de confirmar | Alerta genérica reactiva tras rechazo del backend (409) | 🟡 | Agregar bloqueo preventivo client-side + conservar alerta del backend (HU-08) |
| Total | `Total a Pagar` destacado `text-3xl` color primario | Label `Total` normal | ❌ | Alinear jerarquía visual |
| Botones footer | `Cancelar` + `Confirmar Venta` (disabled con candado cuando hay stock insuficiente) | Solo `Confirmar venta` / `Procesando...` | 🟡 | Agregar `Cancelar` y estado bloqueado con candado |

### HU-02 + HU-04 — Gestión de Cambios (`mockup_hu02_hu04.html`) → placeholder `/cambios`

**Estado global: ❌ / ⛔ (decisión D-003).** Solo existe placeholder
`"{page} — Próximamente"`. Elementos contractuales a implementar cuando haya backend:

- Título: `Gestión de Cambios y Devoluciones`
- Paso 1 badge circular: `Validar Comprobante (Obligatorio)`
- Placeholder ticket: `Escanear o ingresar N° de Ticket` (input mono)
- Botón: `Validar`
- Estado válido: caja verde `Ticket Encontrado: {nro}` + `Fecha de compra: ...` + badge `✅ N / 15 días transcurridos` + caption `Dentro del plazo permitido` + tabla `Producto · Cant. · Precio`
- Estado vencido (alternativo): badge rojo `⚠️ N / 15 días transcurridos` + alerta `border-l-4`: `Plazo de cambio vencido` + `La política de la empresa solo permite cambios hasta 15 días después de la compra.`
- Botones: `Cancelar` · `Continuar con el Cambio` / estado bloqueado `Cambio No Permitido`

### HU-03 — Inspección de Producto (`mockup_hu03.html`) → sin pantalla

**Estado global: ❌ / ⛔ (decisión D-003).** Elementos contractuales:

- Título: `Inspección de Producto para Cambio`; contexto `Ticket: {nro} \| Cajero: {nombre}`
- Checklist: checkbox `¿El producto conserva su etiqueta original intacta?` + hint `Verificar que no esté cortada, arrancada o adulterada.`
- Select `Estado físico del producto:` con opciones emoji: `🟢 Nuevo / Sin señales de uso (Apto)` · `🟡 Con leves señales de uso (No apto)` · `🔴 Dañado o sucio (No apto)`
- Textarea requerido: `Observaciones del cajero *`
- Estado apto: `Producto apto para cambio` + texto completo del contrato
- Estado rechazado (alternativo): `Producto NO apto para cambio` + botón `Rechazar Cambio (No permitido)`
- Botones: `Cancelar Cambio` · `Aprobar Inspección y Continuar`

### HU-05 — Control de Descuentos (`mockup_hu05.html`) → modal en `/ventas`

Flujo estructural divergente → **decisión D-002**: se conserva el flujo post-venta
del endpoint real; la UI se adapta a la estética del mockup.

| Elemento | Contrato (texto exacto) | Frontend actual | Estado | Acción |
| :--- | :--- | :--- | :--- | :--- |
| Modal autorización | Header naranja: `Autorización Requerida` + `El descuento del {N}% supera el límite permitido (20%).` | Título blanco `Aplicar descuento` + Alert warning propio | 🟡 | Rediseñar header naranja con texto contractual |
| Hint límite | `(Máx. 20% sin autorización)` junto al label | Warning solo si supera 20% | 🟡 | Mostrar hint siempre |
| Campos gerente | `ID de Usuario / Correo del Gerente` + `Contraseña o PIN de Autorización` | `ID del gerente autorizador *` + `Motivo del descuento *` | 🟡 | Mantener campos del endpoint (D-002); alinear labels al tono del contrato |
| Botón aplicar | `Aplicar` (oscuro `bg-gray-800`) | Botón secondary post-venta | 🟡 | Estilo oscuro para acción Aplicar |
| Confirmación bloqueada | `Confirmar Venta` disabled mientras descuento pendiente | No aplica (post-venta) | 🟡 | Desviación aceptada (D-002) |
| Error credenciales (alternativo) | `Credenciales de gerente inválidas. Intente nuevamente.` | Usa mensajes centralizados `DESCUENTO_SIN_AUTORIZACION` | ✅ | Cubierto por `apiErrors.ts` |

### HU-06 — Consulta de Stock (`mockup_hu06.html`) → `/productos/stock`

| Elemento | Contrato (texto exacto) | Frontend actual | Estado | Acción |
| :--- | :--- | :--- | :--- | :--- |
| Título página | `Consulta de Stock en Tiempo Real` | `Consulta de Stock` | ❌ | Cambiar texto |
| Header usuario/fecha | `Vendedor: Carlos Ruiz` + `Sistema: 05 Jun 2026 - 14:35` | Header manual simple sin meta | 🟡 | Alinear patrón de header con HU-01 |
| Placeholder búsqueda | `Escanear código o escribir nombre del producto...` | `Buscar por nombre o código (mínimo 3 caracteres)...` | ❌ | Cambiar texto |
| Chip Enter | `Enter para buscar` | kbd `Enter` | 🟡 | Ajustar texto del chip |
| Encabezado resultados | `Resultados encontrados (N)` | `ResultsHeader` con count | ✅ | — |
| Card resultado | Icono de caja + nombre + `Código: X \| Categoría: Y` + badge derecha | Nombre + metadatos, sin icono | 🟡 | Agregar icono de categoría |
| Timestamp actualización | `Última actualización: hace 2 min` | Ausente | ⛔ | Omitido por D-004 (backend no lo expone) |
| Badge stock 3 niveles | Verde `24 en stock` / amarillo `2 en stock` / (rojo agotado) | Binario: en stock / agotado | ❌ | `StockBadge` con nivel bajo (umbral compartido) |
| Estado vacío | `Producto no encontrado` + `No existe ningún producto activo con el código o nombre "X".` + `Verifique el código de barras o intente con otra palabra clave.` | `No se encontraron productos` + genérico | ❌ | Adoptar textos del contrato (con la query interpolada) |

### HU-07 — Ticket de Venta (`mockup_hu07.html`) → `TicketCard` en `/ventas`

| Elemento | Contrato (texto exacto) | Frontend actual | Estado | Acción |
| :--- | :--- | :--- | :--- | :--- |
| Estructura | Card vertical centrado `max-w-md` `shadow-2xl` | Card embebida en columna derecha | 🟡 | Evaluar presentación post-venta centrada |
| Header éxito | Verde: check circular + `¡Venta Registrada!` + `La operación se guardó correctamente en el sistema.` | Borde verde, eyebrow `Comprobante de Venta` | ❌ | Agregar header de éxito contractual |
| Branding | `TIENDA RETAIL S.A.` · `RUC: 20123456789` | Ausente | ❌ | Agregar encabezado de empresa |
| Fuente ticket | `JetBrains Mono` | `font-mono` default | 🟡 | Token tipográfico mono (Fase 2) |
| Ítems | `1x Camiseta Básica Azul → $25.00` | Tabla `Producto · Cant. · Precio · Subtotal` | 🟡 | Simplificar al formato del comprobante |
| Total | `TOTAL → $110.00` | `TOTAL` + monto | ✅ | — |
| Comprobante N° | `COMPROBANTE N°` → `T-20260605-142` | Número ticket mono bold | 🟡 | Etiquetar como `COMPROBANTE N°` |
| Botones | `Imprimir Comprobante` + `Nueva venta` | `Imprimir ticket` + `Nueva venta` | 🟡 | Cambiar texto |
| Toast impresora (alternativo) | Naranja `Advertencia de Impresión` + `La venta se registró, pero la impresora está desconectada. ¿Desea reintentar?` + link `Reintentar impresión` | Ausente | ❌ | Simular fallo de impresión con toast (la venta ya está registrada) |

## 3. Estados alternativos obligatorios (comentarios HTML del contrato)

Los mockups no tienen JS: cada estado alternativo está documentado como
comentario HTML ("Descomentar para ver"). **Todos deben implementarse con su
test unitario correspondiente.**

| # | Pantalla | Estado alternativo | Test requerido |
| :--- | :--- | :--- | :--- |
| E-01 | HU-01 | Carrito bloqueado por ítem sin stock (visible en el estado default) | Venta deshabilitada + alerta preventiva visible |
| E-02 | HU-02/04 | Ticket vencido (>15 días): badge rojo + `Plazo de cambio vencido` | Bloqueado por D-003 |
| E-03 | HU-03 | Producto rechazado: `Producto NO apto para cambio` + botón rechazo | Bloqueado por D-003 |
| E-04 | HU-05 | Descuento dentro del límite: línea verde sin modal | Modal NO aparece con ≤20% |
| E-05 | HU-05 | Credenciales inválidas del gerente | Error mostrado y registro exigido |
| E-06 | HU-06 | Búsqueda vacía: `Producto no encontrado` con query interpolada | Estado vacío con textos exactos |
| E-07 | HU-07 | Toast `Advertencia de Impresión` + reintento (venta ya registrada) | Toast visible; venta permanece exitosa |

## 4. Backlog HU-08 integrado a esta iteración

Según `docs/04_historias_usuario/HU-08/HU-08_frontend_backlog.md`:

1. `apiErrors.ts`: agregar `ERROR_ACTUALIZACION_STOCK` (409) y
   `CANTIDAD_MOVIMIENTO_INVALIDA` (422) con los mensajes textuales de la doc.
2. Toast verde de éxito: `Operación exitosa. Inventario actualizado` /
   `Venta registrada e inventario actualizado`.
3. Spinner durante la transacción completa.
4. Feedback post-devolución: bloqueado por D-003 (sin pantalla de cambios).

## 5. Limpiezas técnicas detectadas

| Problema | Ubicación | Acción |
| :--- | :--- | :--- |
| Starter de Vite muerto | `App.tsx`, `App.css` | Eliminar (no los importa `main.tsx`) |
| `cn()` duplicado localmente | `EmptyState`, `ResultsHeader`, `StockBadge`, `StockResultCard`, `PageHeader` | Importar desde `utils/cn.ts` |
| Componente huérfano | `StockResultCard` | Evaluar: eliminar o convertir en base de las cards de resultado |
| Límite de descuento hardcodeado | `DescuentoModal` (`LIMITE_SIN_AUTORIZACION = 20`) | Centralizar constante; idealmente provenir del backend |
| `index.html` sin branding | `lang="en"`, `<title>frontend</title>` | `lang="es"` + título SGVIR |
| Mensaje de error duplicado | `useBuscarProductos` hardcodea fallback distinto | Unificar con `apiErrors.ts` |
