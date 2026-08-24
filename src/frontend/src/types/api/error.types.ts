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
  | 'BUSQUEDA_INVALIDA'
  | 'TICKET_DUPLICADO'
  | 'DESCUENTO_EXCEDE_LIMITE'
  | 'DESCUENTO_SIN_AUTORIZACION'
  | 'DESCUENTO_INVALIDO'
  | 'VENTA_NO_ENCONTRADA'
  | 'TICKET_NO_ENCONTRADO'
  | 'VENTA_YA_EN_CAMBIO'
  | 'PLAZO_VENCIDO'
  | 'CAMBIO_NO_ENCONTRADO'
  | 'PRODUCTO_NO_APTO'
  | 'OBSERVACIONES_REQUERIDAS'
  | 'ERROR_DE_DOMINIO';