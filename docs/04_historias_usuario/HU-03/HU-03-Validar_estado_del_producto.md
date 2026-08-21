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
  - "[[Media prioridad - Stock]]"
fecha_creacion: 2026-08-20
agent_context: true
resumen: "Tarjeta Trello con la metodologuia agil Kanban "
---

# HU-03 - Validar estado del producto

## Descripción

Como vendedor, quiero validar el estado del producto
para aceptar solamente productos sin uso.

Criterios de aceptación:

  - [] Dado que el producto tiene etiqueta, debe permitirse

  - [] Dado que el producto está usado, debe rechazarse

  - [] Dado que falta la etiqueta, el sistema debe bloquear el cambio

Specification by Example
 
  - Producto nuevo y etiquetado = cambio válido
  - Producto usado = cambio rechazado

Acceptance TDD

  - Validar estado del producto y existencia de etiqueta
  - Probar rechazo de productos dañados

## Backend

  - [] Crear validación de estado

  - [] Registrar rechazo de productos

  - [] Validar existencia de etiqueta

## Frontend

  - [] Crear selector de estado

  - [] Mostrar validaciones visuales

  - [] Mostrar mensajes de rechazo


