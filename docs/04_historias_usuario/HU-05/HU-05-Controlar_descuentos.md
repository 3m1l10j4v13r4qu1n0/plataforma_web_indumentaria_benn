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
  - "[[Alta prioridad - Descuentos]]"
fecha_creacion: 2026-08-20
agent_context: true
resumen: "Tarjeta Trello con la metodologuia agil Kanban "
---

# HU-05 - Controlar descuentos

## Descripción

Como gerente, quiero controlar descuentos
para evitar pérdidas económicas.

Criterios de aceptación:

   - Dado que el descuento es válido, debe aprobarse

   - Dado que supera el límite, debe pedir autorización

   - Dado que se aprueba el descuento, debe registrarse el usuario

Specification by Example

   - Descuento 10% = aprobado
   - Descuento 40% = requiere autorización

Acceptance TDD

   - Validar porcentaje permitido
   - Verificar solicitud de autorización y registrar usuario autorizador


## Backend 

   - [] Crear validación de porcentajes

   - [] Crear permisos de autorización

   - [] Registrar auditoría de descuentos


## Frontend

   - [] Crear modal de autorización

   - [] Mostrar alertas de límites

   - [] Mostrar confirmación visual





