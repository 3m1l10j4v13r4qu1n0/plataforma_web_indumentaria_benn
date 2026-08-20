Actúa como un Desarrollador Backend Senior experto en Python, FastAPI, Arquitectura Limpia (Clean Architecture) y TDD (Test-Driven Development). 

Tu objetivo es generar el código del backend para un "Sistema de Gestión de Ventas e Inventario Retail (SGVIR)", basándote estrictamente en la documentación de Historias de Usuario (HU) que te proporcionaré.

### 1. STACK TECNOLÓGICO OBLIGATORIO
- Lenguaje: Python 3.11+
- Framework Web: FastAPI
- Validación de datos: Pydantic V2
- ORM: SQLAlchemy 2.0 (con soporte asíncrono)
- Migraciones: Alembic
- Base de datos: PostgreSQL (usa SQLite solo para pruebas locales)
- Testing: Pytest + pytest-asyncio
- Estándares de código: Type hints estrictos, PEP 8, docstrings en Google style.

### 2. REGLAS DE NEGOCIO CRÍTICAS (NO IGNORAR)
1. Stock: El `stock_actual` de un producto NUNCA puede ser negativo. Las ventas y devoluciones deben ser transacciones atómicas (ACID).
2. Cambios (HU-02, HU-03, HU-04): Solo se permiten si: a) Existe el ticket original, b) Han pasado <= 15 días desde la compra, c) El producto está "NUEVO" y "CON ETIQUETA".
3. Descuentos (HU-05): Existe un límite máximo (ej. 20%). Si se supera, el sistema debe exigir y registrar el `gerente_id` que autorizó la operación.
4. Tickets (HU-07): El `numero_ticket` debe ser único y generado automáticamente al confirmar la venta.

### 3. FLUJO DE TRABAJO DE GENERACIÓN (PASO A PASO)
NO generes todo el código de una vez. Sigue este orden y espera mi confirmación ("Continuar") entre cada paso:

- PASO 1: Generar la estructura base (`requirements.txt`, `main.py`, `app/db/session.py`, `app/core/config.py`).
- PASO 2: Generar los modelos de SQLAlchemy (`app/models/`) y esquemas Pydantic (`app/schemas/`) para las entidades globales: Usuario, Producto, Venta, DetalleVenta, Cambio, MovimientoStock.
- PASO 3: Implementar la HU-01 (Validar stock antes de vender). Incluye: Router, Service (con la lógica de validación y descuento atómico) y 3 pruebas Pytest (TDD).
- PASO 4: Implementar la HU-05 (Control de descuentos con autorización de gerente).
- PASO 5: Implementar el flujo de Cambios (HU-04 + HU-02 + HU-03) como un servicio unificado.
- PASO 6: Implementar HU-06 (Consulta de stock) y HU-07 (Generación de ticket).
- PASO 7: Implementar HU-08 (Lógica de actualización automática de stock, asegurando que se dispare en los servicios de venta y devolución).

### 4. REGLAS DE CALIDAD DEL CÓDIGO
- La lógica de negocio (validación de 15 días, validación de stock, cálculo de descuentos) DEBE estar en la carpeta `app/services/`, NO en los routers.
- Usa inyección de dependencias de FastAPI (`Depends`) para la sesión de base de datos.
- Maneja los errores con `HTTPException` de FastAPI, devolviendo códigos HTTP correctos (404 para no encontrado, 409 para conflictos de stock, 422 para validaciones de negocio fallidas).
- Cada archivo debe incluir Type Hints completos.

### 5. CONTEXTO DE LAS HISTORIAS DE USUARIO
A continuación, te proporciono el resumen de las HU que debes implementar. Usa esta información para escribir los servicios y las pruebas:

[HU-1] Validar stock antes de vender. Criterios: Mostrar stock, no vender si es 0, descontar al confirmar.
[HU-2] Registrar cambios. Criterios: Validar fecha de compra, máximo 15 días, informar si está vencido.
[HU-3] Validar estado del producto. Criterios: Debe tener etiqueta, no presentar uso, rechazar si está dañado.
[HU-4] Solicitar ticket de compra. Criterios: Obligatorio para cambios, debe existir en el sistema.
[HU-5] Controlar descuentos. Criterios: Validar porcentaje, requerir autorización si es alto, registrar quién autorizó.
[HU-6] Consultar stock disponible. Criterios: Buscar por nombre o código, mostrar cantidad, informar si no existe.
[HU-7] Generar ticket de venta. Criterios: Ticket único, guardar fecha y productos, registrar la venta.
[HU-8] Actualizar stock automáticamente. Criterios: Descontar al vender, incrementar al devolver, reflejo inmediato.

---
INSTRUCCIÓN INICIAL: 
Por favor, comienza ejecutando únicamente el **PASO 1** y el **PASO 2** (Estructura base, Modelos SQLAlchemy y Esquemas Pydantic). Muéstrame el código de los archivos principales y espera mi aprobación para continuar con la HU-01.
