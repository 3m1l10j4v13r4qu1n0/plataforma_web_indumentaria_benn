# Contrato Visual con Mockups — SGVIR

Los mockups HTML en [`docs/05_mockups/`](/docs/05_mockups/) son el **contrato
visual aprobado por el cliente**. Esta regla define cómo implementar y evolucionar
el frontend respetando ese contrato. La auditoría de cumplimiento vigente está en
[`docs/05_mockups/AUDITORIA_CUMPLIMIENTO.md`](/docs/05_mockups/AUDITORIA_CUMPLIMIENTO.md).

## Flujo de trabajo obligatorio

1. **Antes de crear o modificar una pantalla**, leer su mockup correspondiente y
   transcribir los textos EXACTOS: títulos de página, labels de formularios,
   placeholders, columnas de tablas, textos de botones y mensajes.
2. **Textos literales = contrato duro.** No se parafrasean, traducen ni "mejoran".
   Toda divergencia textual respecto al mockup es un bug de UI, salvo que esté
   registrada como decisión en la auditoría.
3. **Estados alternativos comentados en el HTML** (`<!-- Descomentar para ver -->`)
   son estados funcionales obligatorios: cada uno se implementa Y tiene su test
   unitario (ver tabla E-01..E-07 en la auditoría).
4. **Design tokens solo en `src/frontend/src/index.css`** (`@theme` de Tailwind v4).
   Prohibido hardcodear hex, fuentes o umbrales dentro de componentes; usar las
   clases token (`brand-*`, `green-*`, `orange-*`, `red-*`) y constantes compartidas.
5. **Formato centralizado**: moneda (`$XX.XX`), fechas es-AR y badges de stock se
   renderizan con los helpers/constants compartidos (`utils/format.ts`), nunca
   inline en cada componente.
6. **Desviación mockup ↔ backend**: cuando el contrato visual exija algo que la
   API no soporta (endpoint inexistente, dato no expuesto), NO se improvisa:
   - Si es del lado backend → queda en backlog (ej. pantallas HU-02/03/04).
   - Si es estético → se adapta la UI al mockup manteniendo el endpoint real.
   - En ambos casos se registra la decisión (D-XXX) en la auditoría antes de codear.

## Checklist de cierre por iteración de pantalla

- [ ] Textos idénticos a los del mockup (labels, placeholders, botones, mensajes).
- [ ] Todos los estados alternativos aplicables implementados + testeados.
- [ ] Sin hex/fuentes/umbrales hardcodeados fuera de tokens y constantes.
- [ ] `npm run lint` sin errores.
- [ ] `npm run build` compila (tsc strict).
- [ ] `npm run test` verde.
- [ ] Auditoría actualizada: elementos pasan a ✅ o quedan con decisión D-XXX.
