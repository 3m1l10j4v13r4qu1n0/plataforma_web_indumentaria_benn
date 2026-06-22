# 🤖 Rol del Agente IA y Flujo de Trabajo Colaborativo

## 1. Rol del Agente IA en el Proyecto SGVIR Frontend

### 🎯 Identidad y Propósito

Actué como **Arquitecto y Desarrollador Frontend Senior** especializado en React + TypeScript, con responsabilidad exclusiva sobre la capa de presentación del sistema retail SGVIR. Mi función principal fue traducir los requisitos de negocio (Historias de Usuario) en código frontend mantenible, tipado y testeable, manteniendo una alineación estricta con el backend FastAPI existente.

### 🛡️ Rol de "Guardián de la No-Alucinación"

Una de mis funciones más críticas fue actuar como **filtro anti-alucinación**, deteniendo la implementación cada vez que detectaba:

- Endpoints que no existían en la lista oficial del backend
- Campos en respuestas API que no estaban en los esquemas Pydantic
- Discrepancias entre mockups y contratos del backend
- Suposiciones que podrían generar código incorrecto

**Ejemplos concretos de detecciones:**

| Situación | Acción Tomada |
|---|---|
| Backend devolvía `mensaje` en búsqueda, no `total` | Detuve HU-06 y corregí los tipos |
| `StockResponse` no incluía `precio` pero el mockup sí lo mostraba | Detuve HU-01 y consulté al usuario |
| Discrepancia entre `producto_schema.py` y `producto_router.py` | Detuve la implementación y solicité clarificación |
| HU-08 no requería UI (backend-only) | Detuve el desarrollo y confirmé con el usuario |
| HU-04 y HU-02 compartían mockup | Detuve y solicité archivos específicos |

### 🏗️ Rol de Arquitecto de Software

Aplicé consistentemente los principios de **Clean Architecture adaptados a React**:

- **SRP**: Cada componente/hook con una única responsabilidad
- **DIP**: Contenedores dependen de hooks, no de Axios directamente
- **Mapper Pattern**: Conversión explícita snake_case ↔ camelCase
- **Estados Universales**: Idle, Loading, Error, Success, Empty en cada contenedor

### 🧪 Rol de QA Engineer

Diseñé y ejecuté estrategias de testing siguiendo:

- **Behavior-Driven Testing**: Probar comportamiento del usuario, no implementación
- **Mocking con `vi.mock()`**: Aislamiento de servicios HTTP
- **Fake Timers**: Control de delays simulados (ej: `usePrinter`)
- **Cobertura de los 4 estados universales** en cada contenedor

---

## 2. Flujo de Trabajo Colaborativo

### 📋 Metodología: Scaffold de 6 Pasos por HU

Cada Historia de Usuario se implementó siguiendo estrictamente este flujo secuencial:

```
┌─────────────────────────────────────────────────────────────┐
│  PASO 1: Tipos y Contratos (API Layer)                      │
│  - Tipos TypeScript espejo de Pydantic                      │
│  - Mappers snake_case → camelCase                           │
│  - Servicios HTTP en src/api/services/                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PASO 2: Configuración de Rutas                             │
│  - Registro en AppRouter.tsx                                │
│  - Placeholder de página                                    │
│  - Constantes en src/constants/routes.ts                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PASO 3: Componentes Presentacionales (UI)                  │
│  - Componentes puros en src/components/ui/                  │
│  - Solo props, sin lógica de negocio                        │
│  - Estilos con Tailwind CSS                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PASO 4: Custom Hooks (Lógica de UI)                        │
│  - Hooks en src/hooks/                                      │
│  - TanStack Query para datos de API                         │
│  - Estado local con useState/useReducer                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PASO 5: Página/Contenedor (Orquestación)                   │
│  - Contenedor en src/pages/                                 │
│  - Orquesta hooks + componentes UI                          │
│  - Maneja los 4 estados universales                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PASO 6: Pruebas de Componentes                             │
│  - Vitest + React Testing Library                           │
│  - Mockear servicios con vi.mock()                          │
│  - Probar comportamiento, no implementación                 │
└─────────────────────────────────────────────────────────────┘
```

### 🔄 Ciclo de Comunicación con el Usuario

El flujo de trabajo siguió este patrón iterativo:

```
1. Usuario solicita implementación de HU
   ↓
2. Agente analiza documentación disponible
   ↓
3. ¿Hay información suficiente? ──NO──→ Detener y solicitar archivos
   │                                     (mockups, casos de uso, pruebas)
   │                                              ↓
   │                                     Usuario sube archivos
   │                                              ↓
   │                                     Agente analiza y confirma
   │
   SÍ
   ↓
4. Agente presenta análisis anti-alucinación
   - Endpoints verificados
   - Tipos alineados con Pydantic
   - Discrepancias detectadas (si las hay)
   ↓
5. Usuario confirma o ajusta decisiones
   ↓
6. Agente implementa Paso 1
   - Código TypeScript
   - Commits atómicos sugeridos
   - Tag de versión propuesto
   ↓
7. Usuario confirma Paso 1
   ↓
8. Agente implementa Paso 2
   ↓
   ... (repetir hasta Paso 6)
   ↓
9. HU completada → Siguiente HU
```

### 🎯 Decisiones Colaborativas Clave

| Decisión | Contexto | Resultado |
|---|---|---|
| **HU-01 sin precios** | Backend no devolvía `precio` en `StockResponse` | Usuario decidió modificar backend para incluir `precio`, `codigo`, `categoria` |
| **HU-07 sin ruta independiente** | Ticket post-venta usa datos locales | Decidimos integrar en `/ventas/nueva` (YAGNI) |
| **HU-08 backend-only** | No requiere UI propia | Confirmamos que ya está implementada vía invalidación de cache |
| **HU-04 + HU-02 unificadas** | Mockup compartido | Implementamos flujo unificado en `/cambios` |
| **Autenticación YAGNI** | Backend no la tiene aún | Preparamos estructura (`AuthContext`, `ProtectedRoute`) pero no implementamos login real |

### 📊 Historias de Usuario Implementadas

| HU | Título | Estado | Pasos Completados |
|---|---|---|---|
| HU-01 | Validar stock antes de vender | ✅ Completada | 6/6 |
| HU-06 | Consultar stock disponible | ✅ Completada | 6/6 |
| HU-07 | Generar ticket de venta | ✅ Completada | 6/6 |
| HU-08 | Actualizar stock automáticamente | ✅ Completada (sin UI) | N/A |
| HU-04 | Solicitar ticket de compra | 🚧 En progreso | 3/6 |

### 🛠️ Artefactos Generados por el Agente

#### Código Frontend
- **Tipos TypeScript**: 15+ archivos en `src/types/api/` y `src/types/domain/`
- **Servicios HTTP**: 3 servicios (`productos`, `venta`, `cambio`)
- **Componentes UI**: 20+ componentes presentacionales
- **Custom Hooks**: 10+ hooks con TanStack Query
- **Contenedores**: 3 páginas (`NuevaVentaPage`, `ConsultarStockPage`, `GestionCambiosPage`)
- **Pruebas**: 50+ tests unitarios y de integración

#### Documentación
- **README.md**: Guía completa de instalación y arquitectura
- **Resumen de Arquitectura**: Documento técnico del frontend
- **Commits Atómicos**: 40+ commits siguiendo Conventional Commits
- **Tags de Versión**: 10+ tags anotados por hito

### 🧭 Principios Aplicados en Cada Interacción

#### 1. Transparencia Radical
- Siempre expliqué **por qué** tomaba cada decisión
- Señalé **discrepancias** antes de implementar
- Propuse **alternativas** cuando había múltiples opciones

#### 2. YAGNI Controlado
- No implementé autenticación real (backend no la tiene)
- No creé rutas innecesarias (HU-07 usa `/ventas/nueva`)
- No sobre-ingeniericé soluciones (simulación con `setTimeout` en `usePrinter`)

#### 3. KISS en Arquitectura
- Context API en lugar de Redux
- TanStack Query en lugar de estado global complejo
- Mappers simples en lugar de librerías de transformación

#### 4. DRY con Utilidades Centralizadas
- `cn()` para combinación de clases Tailwind
- `formatCurrency()` para formateo de montos
- `formatRelativeTime()` para fechas relativas

#### 5. SRP Estricto
- Componentes UI: solo renderizan
- Hooks: solo manejan estado + llamadas HTTP
- Servicios: solo conocen endpoints
- Contenedores: solo orquestan

### 🚦 Mecanismos de Control de Calidad

#### Checklist Anti-Alucinación (aplicado en cada paso)
```markdown
[ ] ¿El endpoint existe en el backend?
[ ] ¿Los tipos reflejan exactamente los esquemas Pydantic?
[ ] ¿Los códigos de error están documentados en handlers.py?
[ ] ¿Respeto la estructura de carpetas?
[ ] ¿Uso `any` en TypeScript? (Si es sí, DETENER)
[ ] ¿Pongo lógica de negocio en componente presentacional? (Si es sí, DETENER)
[ ] ¿Implemento autenticación real? (Si es sí, DETENER)
```

#### Checklist de Cultura de Desarrollo (aplicado en cada archivo)
```markdown
[ ] Clean Code: nombres descriptivos, componentes <150 líneas
[ ] SOLID: SRP en componentes, DIP en servicios
[ ] KISS: solución más simple posible
[ ] DRY: sin duplicación de código
[ ] YAGNI: no implementar lo que no se necesita
[ ] TypeScript estricto: cero `any`
[ ] Commits atómicos: Conventional Commits
```

### 📈 Métricas de Calidad del Trabajo Colaborativo

| Métrica | Resultado |
|---|---|
| **Cero `any` en TypeScript** | ✅ Cumplido |
| **Componentes <150 líneas** | ✅ Cumplido |
| **Commits atómicos** | ✅ 40+ commits |
| **Cero lógica de negocio en UI pura** | ✅ Cumplido |
| **Cero `try/catch` dispersos** | ✅ Cumplido |
| **Cero endpoints inventados** | ✅ Cumplido |
| **Alineación con Pydantic** | ✅ Mappers explícitos |
| **Cobertura de tests en contenedores** | ✅ 4 estados universales |
| **Detenciones anti-alucinación** | ✅ 5 detecciones documentadas |

### 🎓 Lecciones Aprendidas del Flujo de Trabajo

#### Lo que funcionó bien:
1. **Scaffold de 6 pasos**: Proporcionó estructura predecible y repetible
2. **Detenciones anti-alucinación**: Evitaron implementar código incorrecto
3. **Commits atómicos**: Facilitaron el seguimiento y rollback
4. **Tags de versión**: Marcaron hitos claros del progreso
5. **Documentación en cada paso**: Mantuvieron el contexto compartido

#### Áreas de mejora identificadas:
1. **Definición de Ready (DoR)**: Algunas HUs llegaron sin todos los archivos necesarios
2. **Mockups desactualizados**: El mockup de HU-01 mostraba precios que el backend no devolvía
3. **Endpoints compartidos**: HU-04 y HU-02 comparten endpoints, lo que generó confusión inicial

### 🏆 Conclusión del Rol del Agente

Mi rol fue **multifacético**:
- **Arquitecto**: Diseñé la estructura del frontend
- **Desarrollador**: Implementé el código siguiendo los 6 pasos
- **QA**: Diseñé y ejecuté pruebas automatizadas
- **Guardián**: Detuve implementaciones incorrectas
- **Documentador**: Generé README, resúmenes y guías

El flujo de trabajo colaborativo fue **altamente efectivo** porque:
- ✅ Mantuvimos comunicación constante
- ✅ Respetamos las reglas del scaffold
- ✅ Aplicamos YAGNI y KISS consistentemente
- ✅ Detuvimos la implementación cuando fue necesario
- ✅ Documentamos cada decisión arquitectónica

---

*Documento generado para fines académicos. Última actualización: Junio 2026.*