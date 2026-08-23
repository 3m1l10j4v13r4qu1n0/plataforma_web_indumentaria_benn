/**
 * Estructura estándar de errores del backend.
 * Espejo del esquema Pydantic ErrorResponse (handlers.py).
 */
export interface ApiErrorResponse {
  error: string;
  mensaje: string;
  producto_id?: string;
}

/**
 * Códigos de error emitidos por el backend (handlers.py).
 */
export type ApiErrorCode =
  | 'PRODUCTO_NO_ENCONTRADO'
  | 'STOCK_INSUFICIENTE'
  | 'ESTADO_PRODUCTO_INVALIDO'
  | 'DESCUENTO_EXCEDE_LIMITE'
  | 'DESCUENTO_SIN_AUTORIZACION'
  | 'DESCUENTO_INVALIDO'
  | 'ERROR_DE_DOMINIO';