opencode# .opencode/rules/ — SGVIR

Reglas separadas por concepto para que opencode Code las respete de forma consistente durante todo el desarrollo del proyecto.

| Archivo                        | Contenido                                                                         |
| ------------------------------ | --------------------------------------------------------------------------------- |
| `stack-tecnologico.md`         | Stack obligatorio (lenguaje, framework, ORM, testing, estándares de código)       |
| `reglas-negocio.md`            | Reglas de negocio críticas (stock, cambios, descuentos, tickets) — no negociables |
| `calidad-arquitectura.md`      | Separación de capas, inyección de dependencias, manejo de errores HTTP            |
| `roadmap-historias-usuario.md` | Plan paso a paso y resumen de las HU-1 a HU-8 (referencia, se va actualizando)    |
| `solid-python.md` | Principios S.O.L.I.D que orientan la generacion de codigo limpio    |

## Cómo referenciarlos desde AGENTS.md

Si tu `AGENTS.md` no carga automáticamente estos archivos, agregá algo así al principio:

```markdown
## Reglas del proyecto

Antes de generar código, revisá:

- .opencode/rules/stack-tecnologico.md
- .opencode/rules/reglas-negocio.md
- .opencode/rules/calidad-arquitectura.md
- .opencode/rules/roadmap-historias-usuario.md
```

Nota: si tu versión de opencode carga automáticamente todo `.opencode/rules/*.md` como contexto persistente, no hace falta el paso anterior — pero conviene verificarlo, ya que este comportamiento puede variar según versión.
