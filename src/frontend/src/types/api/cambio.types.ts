/**
 * Estado físico del producto presentado a cambio (HU-03).
 * Espejo del enum EstadoProducto del dominio del backend.
 */
export type EstadoProducto = 'NUEVO_ETIQUETADO' | 'USADO' | 'DANADO';

/**
 * Request de POST /api/v1/cambios (HU-02).
 * Espejo del esquema Pydantic ProcesarCambioRequest.
 */
export interface ProcesarCambioRequest {
  venta_original_id: string;
  cajero_id: string;
  producto_a_cambiar_id: string;
  nuevo_producto_id: string;
  motivo?: string | null;
}

/**
 * Response de POST /api/v1/cambios (HU-02).
 * Espejo del esquema Pydantic CambioResponse.
 */
export interface CambioResponse {
  id: string;
  venta_original_id: string;
  fecha_cambio: string;
  cajero_id: string;
  producto_a_cambiar_id: string;
  nuevo_producto_id: string;
  estado: string;
  motivo: string | null;
}

/**
 * Estructura de error genérico del módulo cambios.
 * Espejo del esquema Pydantic CambioErrorResponse.
 */
export interface CambioErrorResponse {
  error: string;
  mensaje: string;
}

/**
 * Request de POST /api/v1/cambios/{cambio_id}/validar-estado (HU-03).
 * Espejo del esquema Pydantic ValidarEstadoProductoRequest.
 */
export interface ValidarEstadoProductoRequest {
  producto_id: string;
  estado_producto: EstadoProducto;
  tiene_etiqueta: boolean;
  observaciones?: string | null;
  cajero_id?: string | null;
}

/**
 * Response exitosa de POST /api/v1/cambios/{cambio_id}/validar-estado (HU-03).
 * Espejo del esquema Pydantic ValidarEstadoProductoResponse.
 */
export interface ValidarEstadoProductoResponse {
  mensaje: string;
  es_apto_para_cambio: boolean;
}

/**
 * Error 422 cuando el producto no es apto para el cambio (HU-03).
 * Espejo del esquema Pydantic ProductoNoAptoErrorResponse.
 */
export interface ProductoNoAptoErrorResponse {
  error: string;
  mensaje: string;
  motivo: string;
  es_apto_para_cambio: false;
}
