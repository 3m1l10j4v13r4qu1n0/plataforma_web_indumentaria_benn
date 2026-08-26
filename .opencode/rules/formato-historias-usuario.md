# Formato de Documentación para Historias de Usuario — SGVIR

Toda historia de usuario (HU) DEBE documentarse usando el siguiente formato estandarizado. Cada HU vive en una carpeta propia dentro de `docs/04_historias_usuario/HU-XX-nombre/`.

## Estructura de archivos

Cada HU debe generar **mínimo 1 archivo** y **máximo 6 archivos**, siguiendo esta convención de nombres:

```
docs/04_historias_usuario/HU-XX-nombre/
├── HU-XX-nombre_descriptivo.md          ← Archivo principal (obligatorio)
├── HU-XX_requerimientos.md              ← Requerimientos de interfaz (frontend)
├── HU-XX_api.md                         ← Especificación de endpoints
├── HU-XX_modelos_datos.md               ← Modelos de datos impactados
├── HU-XX_pruebas.md                     ← Plan de pruebas (SBE + TDD)
└── HU-XX_caso_uso_expandido.md          ← Caso de uso detallado con flujos
```

**Regla de inclusión**: Solo crear los archivos que la HU necesite. Si una HU es solo backend (sin UI), no crear `_requerimientos.md`. Si no toca datos, no crear `_modelos_datos.md`. El archivo principal SIEMPRE es obligatorio.

---

## Formato del archivo principal (`HU-XX-nombre_descriptivo.md`)

### Frontmatter YAML (obligatorio)

```yaml
---
tags:
  - proyecto/sgvir
  - area/backend    # si aplica
  - area/frontend   # si aplica
  - tipo/tag-trello
  - stack/fastapi       # stack que usa
  - stack/sqlalchemy
  - stack/react
  - stack/postgresql
status: pendiente       # pendiente | en-progreso | hecho
prioridad: alta         # alta | media | baja
relacionado:
  - "[[Categoria - nombre]]"
fecha_creacion: YYYY-MM-DD
agent_context: true
resumen: "Descripción breve de la HU"
---
```

### Cuerpo del archivo principal

```markdown
# HU-XX - Título descriptivo

## Descripción
Párrafo breve que explique QUÉ se resuelve y POR QUÉ.

## Criterios de Aceptación
Formato Gherkin (Dado/Cuando/Entonces):

- Dado que [contexto], cuando [acción], entonces [resultado esperado].
- Dado que [contexto], cuando [acción], entonces [resultado esperado].

## Specification by Example
- Ejemplo 1: [caso positivo]
- Ejemplo 2: [caso negativo]

## Acceptance TDD
- Probar [escenario 1]
- Probar [escenario 2]

## Backend
- [ ] Tarea 1
- [ ] Tarea 2

## Frontend
- [ ] Tarea 1
- [ ] Tarea 2
```

---

## Formato de archivos complementarios

### `HU-XX_api.md` — Especificación de API

```markdown
# HU-XX: Especificación de API (Título)

## Endpoint 1: Nombre del endpoint
- **Método**: `GET` / `POST` / `PUT` / `DELETE`
- **Ruta**: `/api/v1/recurso`
- **Descripción**: Qué hace este endpoint.
- **Request Body** (si aplica): JSON de ejemplo
- **Respuesta Éxito (2xx)**: JSON de ejemplo
- **Respuesta Error (4xx/5xx)**: JSON de ejemplo con código de error

## Endpoint 2: ...
```

### `HU-XX_modelos_datos.md` — Modelos de datos

```markdown
# HU-XX: Modelos de Datos (Título)

## Entidades Involucradas
### 1. EntidadNombre
- `campo` (Tipo): Descripción. **(Campo crítico)** si es relevante.

## Reglas de Integridad y Base de Datos
- Restricciones a nivel de DB, checks, índices, atomicidad.
```

### `HU-XX_pruebas.md` — Plan de pruebas

```markdown
# HU-XX: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Nombre (Caso Positivo/Negativo/Borde)
- **Dado** que [contexto].
- **Cuando** [acción].
- **Entonces** [resultado].
- **Y** [resultado adicional].

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_nombre_del_test()`
- [ ] `test_otro_test()`
```

### `HU-XX_caso_uso_expandido.md` — Caso de uso

```markdown
# HU-XX: Caso de Uso Expandido (Título)

**Actor Principal**: Rol del usuario
**Precondición**: Estado previo necesario.

## Flujo Principal (Éxito)
1. Paso 1.
2. Paso 2.

## Flujo Alternativo 1: Nombre del flujo alternativo
1. Paso 1.
2. Paso 2.

## Postcondición
- Qué cambia en el sistema después del flujo exitoso.
```

### `HU-XX_requerimientos.md` — Requerimientos de interfaz

```markdown
# HU-XX: Requerimientos de Interfaz (Frontend)

## Reglas de Visualización
- Comportamientos visuales, badges, estados de botones.

## Estados de la Interfaz y Manejo de Errores
- Estados UI, disabled/enabled, toasts, mensajes de error.
```

---

## Reglas generales

1. **Nombrado de archivos**: `HU-XX_descripcion.md` con guiones bajos como separador.
2. **Cada archivo empieza con**: `# HU-XX: Título descriptivo`.
3. **No duplicar contenido**: Si algo ya está en el archivo principal, no repetirlo en complementarios.
4. **Formato Gherkin**: Los criterios de aceptación SIEMPRE usan "Dado/Cuando/Entonces".
5. **Checklists**: Usar `- [ ]` para tareas pendientes, `- [x]` para completadas.
6. **Código inline**: Usar backticks para nombres de campos, endpoints, archivos.
7. **Tablas**: Usar tablas markdown para mapeos (excepciones, endpoints, dependencias).
