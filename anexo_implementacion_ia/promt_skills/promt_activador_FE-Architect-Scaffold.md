# 🎨 Prompt Activador: FE-Architect-Scaffold

Activa la habilidad **FE-Architect-Scaffold**.

Adjunto los archivos actuales del proyecto frontend y el `README.md` de contexto.
Quiero implementar la siguiente funcionalidad/pantalla del frontend:

**[DESCRIBIR FUNCIONALIDAD, ej: Pantalla de Procesamiento de Ventas]**

**Contexto del Backend (para evitar alucinaciones):**
- Backend: FastAPI + Clean Architecture + Hexagonal
- Base de datos: PostgreSQL
- Endpoints disponibles: [LISTAR ENDPOINTS A CONSUMIR, ej: POST /api/v1/ventas]
- Autenticación: **AÚN NO IMPLEMENTADA** (preparar estructura, pero no implementar login real)

Por favor, guíame o genera el código siguiendo estrictamente los **6 Pasos del FE-Architect-Scaffold**, respetando:

✅ **La estructura de carpetas definida** (`src/api/`, `src/components/`, `src/pages/`, `src/hooks/`, etc.)
✅ **La regla de no-alucinación**: Solo consumir endpoints documentados en el backend.
✅ **La separación de responsabilidades**: Componentes presentacionales vs contenedores vs hooks.
✅ **El manejo centralizado de errores HTTP** (interceptor de Axios + ErrorBoundary).
✅ **Tipado estricto con TypeScript** (sin `any`, tipos alineados con Pydantic del backend).
✅ **La preparación para autenticación futura** (AuthContext vacío, ProtectedRoute, interceptor de token).

---

## 🔥 Activación Obligatoria de la Cultura de Desarrollo (Developer Culture)

Para cada nuevo archivo, componente, hook o funcionalidad generada, activa y aplica automáticamente la sección **Cultura de Desarrollo de Software** de la habilidad **FE-Architect-Scaffold**.

En particular, todo el código generado debe cumplir con:

### Principios de diseño
- ✅ Clean Code
- ✅ SOLID (especialmente SRP en componentes)
- ✅ KISS (solución más simple posible)
- ✅ DRY (no duplicar componentes/lógica)
- ✅ YAGNI (no implementar lo que no se necesita aún)

### Calidad del código
- ✅ Nombres descriptivos para componentes, hooks y variables.
- ✅ Componentes pequeños (<150 líneas) con una única responsabilidad.
- ✅ Alta cohesión y bajo acoplamiento.
- ✅ Evitar duplicación de código.
- ✅ Mantener las soluciones simples.
- ✅ No introducir complejidad innecesaria.
- ✅ No implementar funcionalidades no requeridas.

### Convenciones
- ✅ Respetar la estructura del proyecto (`src/api/`, `src/components/`, etc.).
- ✅ Mantener consistencia con los módulos existentes.
- ✅ Generar código fácilmente testeable.
- ✅ Priorizar la legibilidad y mantenibilidad sobre la optimización prematura.
- ✅ **TypeScript estricto**: Prohibido `any`.

### Testing
Siempre que corresponda:
- ✅ Crear o actualizar pruebas de componentes con **Vitest + React Testing Library**.
- ✅ Mockear servicios API con `vi.mock()`.
- ✅ Probar los tres estados universales: Loading, Error, Success.
- ✅ Verificar comportamiento, no implementación.

### Commits
Cuando una implementación requiera varios cambios, sugerir commits atómicos siguiendo la convención **Conventional Commits**, por ejemplo:
```bash
feat: agregar pantalla de procesamiento de ventas
fix: corregir validación de descuento en formulario
refactor: extraer componente de tabla de productos
test: agregar pruebas para hook useBuscarProductos
docs: documentar estructura de carpetas del frontend
```

### Revisión Continua
Antes de dar por terminada una funcionalidad:
- ✅ Revisar que se respeten los principios SOLID.
- ✅ Verificar que no exista lógica duplicada.
- ✅ Comprobar que los tipos TypeScript reflejen exactamente los esquemas Pydantic del backend.
- ✅ Validar que los errores HTTP se manejen centralizadamente (no `try/catch` dispersos).
- ✅ Mantener el código coherente con la arquitectura del proyecto.
- ✅ **Verificar que NO se hayan inventado endpoints ni campos de respuesta**.

---

## 🚦 Instrucciones de Ejecución

1. **Empieza por el Paso 1** (Definición de Tipos y Contratos) y **espera mi confirmación** antes de avanzar al siguiente paso.
2. En cada paso, además de implementar los requisitos funcionales, realiza una **revisión implícita** de las buenas prácticas de la sección Developer Culture, señalando posibles mejoras cuando sea necesario.
3. Si detectas que necesito un endpoint que **no existe en el backend**, **DETÉN la implementación** y notifícame antes de continuar.
4. Al finalizar cada paso, sugiere los **commits atómicos** correspondientes.
5. Al completar la funcionalidad, sugiere un **tag anotado** para marcar el hito.

---

## 📋 Lista de Verificación Anti-Alucinación

Antes de generar código, el agente debe verificar:

- [ ] ¿El endpoint que voy a consumir existe en el backend? (Ver tabla de endpoints en FE-Architect-Scaffold.md)
- [ ] ¿Los tipos TypeScript que voy a crear reflejan exactamente los esquemas Pydantic del backend?
- [ ] ¿Los códigos de error HTTP que voy a manejar están documentados en `handlers.py` del backend?
- [ ] ¿Estoy respetando la estructura de carpetas definida?
- [ ] ¿Estoy usando `any` en TypeScript? (Si es sí, DETENER y corregir)
- [ ] ¿Estoy poniendo lógica de negocio en un componente presentacional? (Si es sí, DETENER y mover a hook)
- [ ] ¿Estoy implementando autenticación real? (Si es sí, DETENER: el backend aún no la tiene)

---

**Comienza con el Paso 1 cuando estés listo.**
```

---
