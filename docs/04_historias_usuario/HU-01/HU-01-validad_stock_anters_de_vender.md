---
tags:
  - proyecto/sgvir
  - area/backend
  - area/frontend
  - tipo/tag-trello
  - stack/fastapi
  - stack/sqlalchemy
  - stack/react
  - stack/postgresql
status: en-progreso
prioridad: alta
relacionado:
  - "[[Categoria - ventas]]"
fecha_creacion: 2026-08-12
agent_context: true
resumen: "Tarjeta Trello con la metodologuia agil Kanban "
---

# HU-01 - Validar stock antes de vender

## Descripción

El sistema debe controlar automáticamente el stock antes de confirmar una venta. Actualmente, a veces se venden productos sin darse cuenta de que no hay stock actualizado.
Criterios de Aceptación

    - Dado que hay un producto en el catálogo, cuando el vendedor intenta venderlo, entonces el sistema debe mostrar el stock disponible del producto.

    - Dado que el stock del producto es cero, cuando el vendedor intenta confirmar la venta, entonces el sistema no debe permitir vender el producto.

    - Dado que la venta de un producto con stock es confirmada, cuando la operación finaliza, entonces el sistema debe descontar el stock automáticamente.

Specification by Example

    - Producto con stock = venta aprobada

    - Producto sin stock = venta rechazada

Acceptance TDD

    - Probar venta con stock disponible

    - Probar venta con stock en cero

## Backend

- [] Crear validación de stock
- [] Crear lógica de descuento de inventario
- [] crear endpoint de validacion
- [] Registrar errores de stock insuficiente
- [] Probar casos limite

# Frontend

- [] Mostrar stock disponible
- [] Mostrar alerta de stock insuficiente
- [] Bloquear boton de venta sin stock
- [] Actualizar vista luego de vander
