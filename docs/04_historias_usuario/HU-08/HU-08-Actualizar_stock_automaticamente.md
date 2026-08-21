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
  - "[[Alta prioridad - Iventario]]"
fecha_creacion: 2026-08-20
agent_context: true
resumen: "Tarjeta Trello con la metodologuia agil Kanban "
---

# HU-08 - Actualizar stock automáticamente

## Descrición

Como encargado de ventas, quiero que el stock se actualice automáticamente
para mantener información correcta del inventario.

Criterios de aceptación:

  - Dado que se realiza una venta, el stock debe descontarse automáticamente

  - Dado que se registra una devolución, el stock debe incrementarse

  - Dado que ocurre una actualización, los cambios deben reflejarse inmediatamente

Specification by Example

  - Venta de 1 producto = stock disminuye en 1
  - Devolución aprobada = stock aumenta en 1

Acceptance TDD

  - Validar descuento de stock al vender (caso positivo)
  - Validar incremento por devolución y actualización en tiempo real (caso negativo/borde)

## Backend 

  - [] Crear servicio de actualización automática de stock

  - [] Descontar stock luego de cada venta

  - [] Incrementar stock en devoluciones

  - [] Validar consistencia de inventario

  - [] Registrar movimientos de stock

  - [] Crear logs de auditoría

  - [] Crear pruebas unitarias del módulo


## Frontend

  - [] Crear servicio de actualización automática de stock

  - [] Descontar stock luego de cada venta

  - [] Incrementar stock en devoluciones

  - [] Validar consistencia de inventario

  - [] Registrar movimientos de stock

  - [] Crear logs de auditoría

  - [] Crear pruebas unitarias del módulo


