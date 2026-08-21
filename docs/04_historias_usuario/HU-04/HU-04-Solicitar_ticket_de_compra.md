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
  - "[[normal prioridad - comprobantes]]"
fecha_creacion: 2026-08-20
agent_context: true
resumen: "Tarjeta Trello con la metodologuia agil Kanban "
---

# HU-04 - Solicitar ticket de compra

## Descripcion

Como cajero, quiero solicitar el ticket de compra
para validar la operación realizada.

Criterios de aceptación:

   - Dado que existe ticket válido, el cambio debe continuar

   - Dado que no existe ticket, el sistema debe rechazar la operación

   - Dado que el ticket está registrado, debe mostrarse la compra

Specification by Example

   - Ticket válido = cambio permitido
   - Ticket inexistente = cambio rechazado

Acceptance TDD

   - Buscar ticket existente
   - Intentar cambio sin ticket y validar mensajes de error

## Backend 

   - [] Crear búsqueda de ticket

   - [] Validar existencia del comprobante

   - [] Crear consulta de ventas


## Frontend

   - [] Crear buscador de ticket

   - [] Mostrar información de compra

   - [] Mostrar errores de validación

