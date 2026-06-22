/**
 * Formatea un número como moneda en pesos argentinos.
 *
 * SRP: Única responsabilidad — formateo de moneda.
 * Pure function: misma entrada → misma salida.
 *
 * @param amount - Monto a formatear
 * @returns String formateado (ej: "$25.00")
 */
export function formatCurrency(amount: number): string {
  if (Number.isNaN(amount)) {
    return '$0.00';
  }
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}
