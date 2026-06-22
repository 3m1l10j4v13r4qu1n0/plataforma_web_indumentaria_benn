# Metodología (Kanban, WIP, flujo y ciclo de desarrollo con IA)

## Aplicación de Kanban en Trello

### Justificativo (por qué usamos Kanban)

Elegimos Kanban porque nos permite **organizar el trabajo por flujo**, visualizar el estado real de cada tarea y **adaptarnos rápido a los cambios** sin frenar el avance del proyecto. Al trabajar con un tablero (Trello) y límites de trabajo en curso (WIP), evitamos tener demasiadas tareas abiertas al mismo tiempo, reducimos bloqueos y mejoramos la coordinación del equipo.

Además, somos un grupo de **4 integrantes** y, aunque cada uno tiene responsabilidades principales, **nos apoyamos y tomamos roles distintos cuando hace falta** para agilizar el desarrollo y cumplir con los tiempos de aplicación:

- **Emilio**: administrador del tablero, testing y backend.
- **Niki**: frontend y diseño.
- **Nely**: backend.
- **Brian**: soporte en distintos roles según necesidad.

Con esta metodología mantenemos un ritmo de entrega constante, priorizamos lo más importante y aseguramos calidad mediante revisiones y pruebas antes de dar una tarea por finalizada.

### Límites WIP definidos

- En proceso: máximo 2 tareas por persona (8 total)
- En revisión: máximo 3 tareas totales

### Flujo de trabajo

1. El admin mueve tareas de Backlog a Pendiente según prioridad
2. Cada desarrollador toma una tarea de Pendiente y la mueve a En proceso
3. Al terminar código, mueve a En revisión y asigna un revisor
4. El revisor valida y mueve a Finalizado
5. Si hay error, vuelve a Pendiente con comentario

### Política de commits en Trello

- Cada tarjeta en En proceso tiene un branch asociado en Git
- El número de tarjeta (ej: HU-01) se usa en el mensaje de commit

---

# **Uso del ciclo de desarrollo con IA en nuestro proyecto**

## **¿Qué es el ciclo de desarrollo?**

El ciclo de desarrollo de software (o SDLC por sus siglas en inglés) son las etapas que seguimos para crear un sistema desde cero: desde entender qué necesita el negocio hasta tener el programa funcionando. Las etapas típicas son: análisis de requisitos, diseño, codificación, pruebas y entrega.

Tradicionalmente, estas etapas las hace un equipo de personas. En nuestro proyecto, decidimos **incorporar herramientas de Inteligencia Artificial (IA)** como apoyo en varias de esas etapas.

## **¿Por qué usamos IA?**

Elegimos usar IA por tres razones principales:

### **1. Acelerar el trabajo**

La IA nos ayuda a generar borradores rápidamente. Por ejemplo, en lugar de escribir 8 historias de usuario desde cero, le pedimos a ChatGPT que nos proponga un borrador y después lo ajustamos. Esto nos ahorra horas de trabajo.

### **2. Reducir errores**

La IA puede detectar inconsistencias o requisitos que faltan. Por ejemplo, cuando escribimos los criterios de aceptación, la IA nos ayudó a identificar casos límite que no habíamos considerado (como "qué pasa si el stock llega a cero justo cuando alguien está comprando").

### **3. Aprender buenas prácticas**

Al usar IA, vemos ejemplos de cómo se escriben historias de usuario, cómo se estructuran pruebas o cómo se documenta un proyecto. Eso nos sirve como referencia para mejorar nuestra forma de trabajar.

## **¿La IA hace todo?**

No. En nuestro equipo, **la IA es una asistente, no la protagonista**.

- La IA **propone** borradores, pero el equipo **decide** qué sirve y qué no.
- La IA **sugiere** código, pero los desarrolladores **revisan y corrigen**.
- La IA **identifica** riesgos, pero los analistas **validan** con el negocio.

En cada caso, documentamos qué herramientas usamos, qué resultado obtuvimos y qué tuvimos que ajustar. Eso es parte de nuestro aprendizaje.

## **¿Cómo aplicamos esto en cada etapa?**

| **Etapa** | **Qué hizo el equipo** | **Qué hizo la IA** |
| --- | --- | --- |
| Análisis de requisitos | Definimos el alcance del sistema y validamos con el negocio. | Nos ayudó a generar un borrador de 8 historias de usuario y a detectar requisitos faltantes. |
| Diseño | Dibujamos los wireframes y el diagrama de clases. | La IA nos propuso una estructura inicial de base de datos en formato Mermaid. |
| Codificación | Escribimos el código de 3 funcionalidades clave. | La IA nos sugirió fragmentos de código y tests unitarios. |
| Gestión de tareas | Organizamos el tablero Kanban en Trello. | La IA nos ayudó a desglosar historias en subtareas. |

## **Reflexión final**

Usar IA en el ciclo de desarrollo no cambia las etapas que tenemos que cumplir. Sigue siendo necesario analizar, diseñar, codificar y probar. Lo que cambia es que ahora tenemos una herramienta que nos hace más rápidos y nos ayuda a evitar errores tontos.

Lo más importante que aprendimos es que **la IA no reemplaza el criterio del equipo**. Una sugerencia de la IA puede estar mal, ser incompleta o no aplicar a nuestro contexto. Siempre tenemos que revisar, ajustar y decidir nosotros.

Para nosotros, el ciclo de desarrollo con IA es simplemente: **las mismas etapas de siempre, pero con un asistente inteligente que nos da una mano**.