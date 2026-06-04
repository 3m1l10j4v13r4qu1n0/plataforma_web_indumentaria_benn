# HU-02: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Cambio dentro del período válido (Caso Positivo)
- **Dado** que un cliente presenta un ticket de compra realizado hace 10 días.
- **Cuando** el cajero ingresa el ticket y solicita procesar el cambio.
- **Entonces** el sistema debe validar la fecha de compra.
- **Y** debe permitir registrar el cambio de producto exitosamente.

## Escenario 2: Cambio con plazo vencido (Caso Negativo)
- **Dado** que un cliente presenta un ticket de compra realizado hace 20 días.
- **Cuando** el cajero ingresa el ticket en el sistema.
- **Entonces** el sistema debe calcular la diferencia de fechas.
- **Y** debe informar con un mensaje claro que el plazo está vencido.
- **Y** no debe permitir avanzar ni procesar el cambio.

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_validar_diferencia_de_fechas_menor_igual_15_dias()`
- [ ] `test_validar_diferencia_de_fechas_mayor_15_dias()`
- [ ] `test_verificar_mensaje_plazo_vencido_en_respuesta_api()`
- [ ] `test_probar_cambio_dentro_del_periodo_valido_registra_en_bd()`
