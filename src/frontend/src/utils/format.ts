/**
 * Helpers de formato visual compartidos (contrato docs/05_mockups/).
 * Formatos deterministas: no dependen del locale del entorno.
 */

const MESES = [
  'Ene',
  'Feb',
  'Mar',
  'Abr',
  'May',
  'Jun',
  'Jul',
  'Ago',
  'Sep',
  'Oct',
  'Nov',
  'Dic',
] as const;

const MESES_COMPLETOS = [
  'Enero',
  'Febrero',
  'Marzo',
  'Abril',
  'Mayo',
  'Junio',
  'Julio',
  'Agosto',
  'Septiembre',
  'Octubre',
  'Noviembre',
  'Diciembre',
] as const;

function pad(n: number): string {
  return String(n).padStart(2, '0');
}

function asegurarDate(fecha: Date | string): Date {
  return typeof fecha === 'string' ? new Date(fecha) : fecha;
}

/**
 * Formatea un monto según el contrato: `$XX.XX` con punto decimal.
 *
 * @param monto Monto a formatear.
 * @returns Monto formateado, ej: `$25.00`.
 */
export function formatoMoneda(monto: number): string {
  return `$${monto.toFixed(2)}`;
}

/**
 * Formatea una fecha como la cabecera de las pantallas del contrato.
 *
 * @param fecha Fecha ISO o instancia de Date.
 * @param opciones `conSegundos` incluye los segundos (ticket HU-07).
 * @returns Ej: `05 Jun 2026 - 14:30` o `05 Jun 2026 - 14:45:30`.
 */
export function formatoFechaCorta(
  fecha: Date | string,
  opciones?: { conSegundos?: boolean },
): string {
  const d = asegurarDate(fecha);
  const segundos = opciones?.conSegundos ? `:${pad(d.getSeconds())}` : '';
  return `${pad(d.getDate())} ${MESES[d.getMonth()]} ${d.getFullYear()} - ${pad(
    d.getHours(),
  )}:${pad(d.getMinutes())}${segundos}`;
}

/**
 * Formatea una fecha detallada como la ficha del ticket/cambio del contrato.
 *
 * @param fecha Fecha ISO o instancia de Date.
 * @returns Ej: `26 de May, 2026 - 10:15 AM`.
 */
export function formatoFechaLarga(fecha: Date | string): string {
  const d = asegurarDate(fecha);
  let horas = d.getHours() % 12;
  if (horas === 0) horas = 12;
  const periodo = d.getHours() < 12 ? 'AM' : 'PM';
  return `${d.getDate()} de ${MESES_COMPLETOS[d.getMonth()]}, ${d.getFullYear()} - ${horas}:${pad(
    d.getMinutes(),
  )} ${periodo}`;
}
