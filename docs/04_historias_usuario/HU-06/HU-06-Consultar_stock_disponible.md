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
prioridad: normal
relacionado:
  - "[[normal prioridad - inentario]]"
fecha_creacion: 2026-08-12
agent_context: true
resumen: "Tarjeta Trello con la metodologuia agil Kanban "
---

# HU-06 - Consultar stock disponible

## Descripción

Como vendedor, quiero consultar stock disponible
para informar correctamente a los clientes.

Criterios de aceptación:

  - Dado que el producto existe, debe mostrarse el stock

  - Dado que no existe, debe mostrar error

  - Dado que el stock cambia, debe actualizarse

Specification by Example

  - Producto existente = muestra cantidad
  - Producto inexistente = mensaje de error

Acceptance TDD

  - Buscar producto válido (caso positivo)
  - Buscar producto inexistente (caso negativo/borde)


## Backend

  - [x] Crear búsqueda de productos
  - [x] Crear consulta de stock
  - [x] Optimizar consultas

## Frontend

  - [] Crear buscador
  - [] Mostrar cantidad disponible
  - [] Mostrar mensajes de error
