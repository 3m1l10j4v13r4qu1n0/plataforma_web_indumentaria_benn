/**
 * Constantes y helpers de stock compartidos (contrato docs/05_mockups/).
 */

/**
 * Umbral bajo el cual el stock se considera "bajo" (badge amarillo).
 * El contrato muestra 2 unidades en amarillo; la API no expone
 * `stock_minimo` en búsquedas, así que se usa este umbral de frontend.
 */
export const UMBRAL_STOCK_BAJO = 5;

export type NivelStock = 'healthy' | 'low' | 'out';

/**
 * Determina el nivel visual de stock a partir de la cantidad.
 *
 * @param stockActual Cantidad actual de unidades.
 * @param umbralBajo Umbral por debajo del cual el stock es "bajo".
 * @returns `out` si es 0, `low` si está debajo del umbral, `healthy` en otro caso.
 */
export function calcularNivelStock(
  stockActual: number,
  umbralBajo: number = UMBRAL_STOCK_BAJO,
): NivelStock {
  if (stockActual === 0) return 'out';
  if (stockActual < umbralBajo) return 'low';
  return 'healthy';
}
