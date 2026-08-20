# Reglas SOLID para generar código Python

## Principios generales
- Cada clase/función debe tener **una única responsabilidad** bien definida. Si hay más de un motivo para cambiar, dividí en módulos/archivos separados.
- Antes de escribir código, pensá en el **contrato** (interfaces/Protocol) antes que en la implementación.
- Preferí **composición sobre herencia**.
- Toda dependencia externa (DB, API, filesystem, random, logging) debe inyectarse vía parámetros o constructores, nunca importarse y usarse directamente dentro de la lógica.
- No aplicar estos principios a rajatabla en todos lados: ver sección "Cuándo NO aplicar SOLID" al final.

## Single Responsibility (S)
- Un módulo = una responsabilidad. No mezclés lógica de negocio con I/O, parsing o persistencia en la misma función.
- Separar capas: `entities` (dominio), `use_cases` (lógica de negocio), `repositories` (persistencia), `interfaces` (Protocol), `utils` (helpers puros).
- Los scripts de entrada (`main.py`, routers de FastAPI) deben orquestar y delegar, no contener lógica de negocio.

## Open/Closed (O)
- El código debe estar **abierto a extensión, cerrado a modificación**. Para agregar comportamiento nuevo, extender con nuevas clases/funciones; no tocar las existentes.
- Usar `typing.Protocol` (o `abc.ABC` cuando aplique, ver sección Dependency Inversion) para definir contratos extensibles, y polimorfismo para variantes.

## Liskov Substitution (L)
- Las subclases o implementaciones de un Protocol deben poder reemplazar al contrato sin romper el comportamiento esperado.
- No sobrescribir métodos base para cambiar la semántica; si hace falta, crear un contrato nuevo.
- Respetar precondiciones/postcondiciones e invariantes del contrato (firma de métodos, tipos de retorno, excepciones esperadas).

## Interface Segregation (I)
- Preferir **interfaces pequeñas y específicas** (`Protocol` con pocos métodos) antes que interfaces grandes con métodos que nadie usa.
- Si una clase no usa todos los métodos de un `Protocol`, dividir el `Protocol` en varios más chicos.

## Dependency Inversion (D)
- Los módulos de alto nivel (use cases) no deben depender de los de bajo nivel (implementaciones concretas de repositorios/servicios); ambos dependen de **abstracciones**.
- Usar `typing.Protocol` para definir puertos/interfaces de repositorios y servicios externos (structural typing, sin herencia forzada). Es el enfoque por defecto en este proyecto.
- Reservar `abc.ABC` + `@abstractmethod` solo cuando se necesite compartir comportamiento concreto entre implementaciones, o forzar un error en runtime si falta un método.
- Las implementaciones concretas (ej. `ProductoRepositorySQLAlchemy`) NO heredan del `Protocol`; solo deben cumplir su firma.
- Inyectar dependencias: pasar instancias por constructor (o vía `Depends` en FastAPI), no instanciar dependencias concretas adentro de las clases.
- El punto de ensamblaje (inicio del programa, factories, `Depends`) es el único lugar permitido para instanciar dependencias concretas.

## Cuándo NO aplicar SOLID a rajatabla
- No crear un `Protocol` para una clase que solo va a tener una implementación real y ningún plan concreto de tener otra.
- No dividir un módulo de pocas líneas solo por "separación de responsabilidades" si la cohesión es alta y no hay motivo de cambio independiente.
- Funciones puras/helpers de `utils` no necesitan inyección de dependencias ni contrato propio.
- DTOs y entidades de dominio simples no necesitan interfaz: son datos, no comportamiento.

## Señales de alerta (smells)
- Clase con muchos métodos públicos y responsabilidades mezcladas → candidata a partir (SRP).
- `isinstance()` / `type()` dentro de lógica de negocio para decidir comportamiento → smell de LSP roto.
- Nombres genéricos tipo `Manager`, `Handler`, `Utils` que terminan acumulando de todo → posible God Object.
- Un `Protocol` con métodos que la mayoría de sus implementaciones no usa → violación de ISP, dividir.
- Un use case que importa directamente `sqlalchemy`, `httpx`, etc. en vez de recibir el repo/cliente inyectado → violación de DIP.

## Verificación
- Al terminar de escribir código, revisar cada principio S-O-L-I-D explícitamente sobre el resultado.
- Validar sintaxis y tipos antes de dar por terminada una tarea:
  ```bash
  venv/bin/python -m py_compile <archivo>.py
  venv/bin/mypy <archivo>.py
  venv/bin/ruff check <archivo>.py
  ```