# HU-05: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Descuento dentro del límite permitido (Caso Positivo)
- **Dado** que el límite de descuento para vendedores es del 20%.
- **Cuando** el vendedor aplica un descuento del 10%.
- **Entonces** el sistema debe aprobar y aplicar el descuento inmediatamente.
- **Y** no debe solicitar credenciales de gerente.

## Escenario 2: Descuento alto sin autorización (Caso Negativo)
- **Dado** que el límite de descuento es del 20%.
- **Cuando** el vendedor intenta aplicar un descuento del 40% sin credenciales de gerente.
- **Entonces** el sistema debe rechazar la aplicación directa.
- **Y** debe solicitar autorización de un usuario con rol de Gerente.

## Escenario 3: Descuento alto con autorización exitosa (Caso Positivo con flujo alternativo)
- **Dado** que se solicita un descuento del 40%.
- **Cuando** un usuario con rol de Gerente ingresa sus credenciales correctamente.
- **Entonces** el sistema debe aplicar el descuento.
- **Y** debe registrar en la base de datos el ID del gerente que autorizó la operación.

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_aplicar_descuento_dentro_del_limite()`
- [ ] `test_rechazar_descuento_alto_sin_autorizacion()`
- [ ] `test_aplicar_descuento_alto_con_credenciales_de_gerente_validas()`
- [ ] `test_verificar_registro_de_usuario_autorizador_en_bd()`
