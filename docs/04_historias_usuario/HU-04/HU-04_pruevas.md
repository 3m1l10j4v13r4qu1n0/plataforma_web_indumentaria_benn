# HU-04: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Ticket válido encontrado (Caso Positivo)
- **Dado** que existe en la base de datos una venta con el ticket "T-20260601-001".
- **Cuando** el cajero ingresa "T-20260601-001" y hace clic en "Validar Ticket".
- **Entonces** el sistema debe mostrar los datos de la compra (fecha y productos).
- **Y** debe habilitar el botón para continuar con el proceso de cambio.

## Escenario 2: Ticket inexistente (Caso Negativo)
- **Dado** que el ticket "T-99999999-999" no existe en el sistema.
- **Cuando** el cajero ingresa ese número y hace clic en "Validar Ticket".
- **Entonces** el sistema debe mostrar el mensaje: "El número de ticket ingresado no existe en el sistema".
- **Y** no debe permitir avanzar en el flujo de cambio.

## Escenario 3: Intento de cambio sin ticket (Caso Negativo / Borde)
- **Dado** que el cliente no presenta ningún comprobante.
- **Cuando** el cajero intenta iniciar un cambio sin ingresar un ticket.
- **Entonces** el sistema debe mantener bloqueado el flujo.
- **Y** debe mostrar un mensaje indicando que el ticket es obligatorio por política de negocio.

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_buscar_ticket_existente_retorna_datos_venta()`
- [ ] `test_buscar_ticket_inexistente_retorna_404()`
- [ ] `test_validar_formato_de_ticket_en_frontend()`
- [ ] `test_verificar_mensaje_error_ticket_no_encontrado()`
- [ ] `test_bloquear_flujo_cambio_sin_ticket_valido()`
