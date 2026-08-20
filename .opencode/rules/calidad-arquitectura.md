# Calidad de Código y Arquitectura — SGVIR

Este proyecto sigue Clean Architecture / Arquitectura Hexagonal / DDD. Estas reglas aplican a TODO el código generado, sin excepción.

## Separación de capas
- La lógica de negocio (validación de 15 días, validación de stock, cálculo de descuentos, reglas de cambio, etc.) DEBE vivir en `app/domain/services/`.
- Los routers (`app/presentation/routers`) NO deben contener lógica de negocio. Solo reciben la request, delegan al service correspondiente y devuelven la respuesta.

## Inyección de dependencias
- Usar `Depends` de FastAPI para inyectar la sesión de base de datos (`AsyncSession`) y otros servicios/repositorios en los endpoints.

## Manejo de errores
- Usar `HTTPException` de FastAPI para errores de la capa de presentación.
- Códigos HTTP correctos:
  - `404` → recurso no encontrado.
  - `409` → conflictos de stock (ej. stock insuficiente).
  - `422` → validaciones de negocio fallidas (ej. descuento excede el límite, cambio fuera de plazo).

## Estándares por archivo
- Cada archivo debe incluir type hints completos (parámetros, retornos, atributos).
- Docstrings en Google style para clases, métodos y funciones públicas.
- Nomenclatura de excepciones y dominio unificada (evitar duplicados; ej. una sola excepción tipo `ProductoInvalidoError` en vez de variantes repetidas).
