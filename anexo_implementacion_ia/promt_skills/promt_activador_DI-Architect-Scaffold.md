Activa la habilidad **DI-Architect-Scaffold**.

Adjunto los archivos actuales del proyecto y el README.md de contexto.

Quiero implementar la siguiente Historia de Usuario:

**[DESCRIBIR HU, ej: HU-01 Alta de Productos]**

Por favor, guíame o genera el código siguiendo estrictamente los **6 Pasos del scaffold**, respetando:

* La estructura de carpetas definida por el proyecto.
* La regla de manejo centralizado de excepciones en `handlers.py`.
* La inyección de dependencias mediante `dependency_injection.py`.
* Los principios de Clean Architecture y Hexagonal Architecture.
* Las reglas inquebrantables del proyecto (SGVIR).

## Activación Obligatoria de la Cultura de Desarrollo de Software

Para cada nuevo archivo, módulo, clase, caso de uso o funcionalidad generada, activa y aplica automáticamente la sección **Cultura de Desarrollo de Software (Developer Culture)** de la habilidad DI-Architect-Scaffold.

En particular, todo el código generado debe cumplir con:

### Principios de diseño

* Clean Code.
* SOLID.
* KISS.
* DRY.
* YAGNI.
* Inversión de Dependencias (DIP).

### Calidad del código

* Nombres descriptivos para clases, funciones y variables.
* Funciones con una única responsabilidad.
* Alta cohesión y bajo acoplamiento.
* Evitar duplicación de código.
* Mantener las soluciones simples.
* No introducir complejidad innecesaria.
* No implementar funcionalidades no requeridas por la Historia de Usuario.

### Convenciones

* Respetar la estructura del proyecto.
* Mantener consistencia con los módulos existentes.
* Generar código fácilmente testeable.
* Priorizar la legibilidad y mantenibilidad sobre la optimización prematura.

### Testing

Siempre que corresponda:

* Crear o actualizar pruebas unitarias.
* Utilizar Fakes o Mocks siguiendo los puertos del dominio.
* Verificar el comportamiento exitoso y los casos de error.

### Commits

Cuando una implementación requiera varios cambios, sugerir commits atómicos siguiendo la convención **Conventional Commits**, por ejemplo:

* `feat: implementar caso de uso de creación de productos`
* `test: agregar pruebas unitarias para CreateProductUseCase`
* `docs: actualizar README con la configuración del módulo`
* `refactor: separar validaciones del dominio`

### Revisión Continua

Antes de dar por terminada una funcionalidad:

* Revisar que se respeten los principios SOLID.
* Verificar que no exista lógica duplicada.
* Verificar que el dominio permanezca desacoplado de FastAPI, SQLAlchemy y Pydantic.
* Comprobar que las excepciones de negocio se manejen exclusivamente en `handlers.py`.
* Mantener el código coherente con la arquitectura del proyecto.

Empieza por el **Paso 1** y espera mi confirmación antes de avanzar al siguiente.

En cada paso, además de implementar los requisitos funcionales, realiza una revisión implícita de las buenas prácticas de la sección **Developer Culture**, señalando posibles mejoras cuando sea necesario.

