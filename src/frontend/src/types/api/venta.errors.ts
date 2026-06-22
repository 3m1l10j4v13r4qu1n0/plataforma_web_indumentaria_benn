import type { ApiErrorCode } from './error.types';

/**
 * Códigos de error específicos de ventas.
 */
export type VentaErrorCode = Extract<
  ApiErrorCode,
  'STOCK_INSUFICIENTE' | 'VALIDACION_ERROR' | 'ERROR_INTERNO'
>;

/**
 * Error estructurado para operaciones de venta.
 */
export interface VentaError {
  code: VentaErrorCode;
  message: string;
  productoId?: string;
}

/**
 * Type guard: verifica si un error es de venta.
 */
export function isVentaError(error: unknown): error is VentaError {
  return (
    typeof error === 'object' &&
    error !== null &&
    'code' in error &&
    'message' in error
  );
}
