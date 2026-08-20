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
prioridad: media
relacionado:
  - "[[Categoria - ventas]]"
fecha_creacion: 2026-08-12
agent_context: true
resumen: "Tarjeta Trello con la metodologuia agil Kanban "
---

# HU-07 - Generar ticket de venta

## Descripción

Como cajero, quiero generar tickets de venta
para entregar comprobantes a los clientes.

Criterios de aceptación:

    - Dado que la venta finaliza, debe generarse ticket

    - Dado que ocurre un error, debe mostrarse advertencia

    - Dado que el ticket existe, debe guardarse en el sistema

## Backend

[] Crear validación de estado
[] Registrar rechazo de productos
[] Validar existencia de etiqueta

## Frontend

[] Crear selector de estado
[] Mostrar validaciones visuales
[] Mostrar mensajes de rechazo
