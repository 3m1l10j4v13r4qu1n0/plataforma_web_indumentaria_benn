import type { ApiErrorCode } from './error.types';

/**
 * Códigos de error específicos del dominio de productos.
 */
export type ProductoErrorCode = Extract<
  ApiErrorCode,
  'PRODUCTO_NO_ENCONTRADO' | 'VALIDACION_ERROR' | 'ERROR_INTERNO'
>;

/**
 * Error estructurado para operaciones de productos.
 */
export interface ProductoError {
  code: ProductoErrorCode;
  message: string;
  details?: Record<string, unknown>;
}

/**
 * Type guard: verifica si un error es de producto.
 */
export function isProductoError(error: unknown): error is ProductoError {
  return (
    typeof error === 'object' &&
    error !== null &&
    'code' in error &&
    'message' in error
  );
}