/**
 * Estructura estándar de errores del backend (handlers.py)
 */
export interface ApiErrorResponse {
  error: string;
  mensaje: string;
  producto_id?: string;
  numero_ticket?: string;
  usuario_id?: string;
}

export type ApiErrorCode =
  | 'STOCK_INSUFICIENTE'
  | 'PLAZO_DE_CAMBIO_VENCIDO'
  | 'PRODUCTO_NO_ELEGIBLE_PARA_CAMBIO'
  | 'TICKET_NO_ENCONTRADO'
  | 'DESCUENTO_NO_AUTORIZADO'
  | 'VALIDACION_ERROR'
  | 'ERROR_INTERNO';