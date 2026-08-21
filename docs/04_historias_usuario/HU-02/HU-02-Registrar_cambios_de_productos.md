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
  - "[[Alta prioridad - Cambios]]"
fecha_creacion: 2026-08-20
agent_context: true
resumen: "Tarjeta Trello con la metodologuia agil Kanban "
---

# HU-02 - Registrar cambios de productos

## Descripción

Como cajero, quiero registrar cambios de productos
para cumplir las políticas del negocio.

Criterios de aceptación:

  - Dado que la compra tiene menos de 15 días, el cambio debe aprobarse
 
  - Dado que el plazo está vencido, el sistema debe rechazar el cambio

  - Dado que el cambio es válido, el stock debe actualizarse

Specification by Example

  - Compra hace 10 días = cambio permitido
  - Compra hace 20 días = cambio rechazado

Acceptance TDD

  - Probar cambio dentro del período válido
  - Verificar mensaje de plazo vencido


## Backend

  - [] Validar fecha de compra

  - [] Crear lógica de cambios

  - [] Actualizar stock automáticamente
  
  - [] Registrar historial de cambios

## Frontend 

  - [] Crear formulario de cambios

  - [] Mostrar validación de plazo

  - [] Mostrar mensajes de error

  - [] Confirmar cambio realizado



