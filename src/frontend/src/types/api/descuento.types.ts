/**
 * Request de POST /api/v1/descuentos.
 * Espejo del esquema Pydantic AplicarDescuentoRequest del backend.
 */
export interface AplicarDescuentoRequest {
  venta_id: string;
  porcentaje: number;
  motivo: string;
  autorizado_por?: string | null;
}

/**
 * Response de POST /api/v1/descuentos.
 * Espejo del esquema Pydantic DescuentoResponse del backend.
 */
export interface DescuentoResponse {
  id: string;
  venta_id: string;
  porcentaje: number;
  monto_descuento: number;
  motivo: string;
  autorizado_por: string | null;
  fecha_aplicacion: string | null;
  requiere_autorizacion: boolean;
  mensaje: string | null;
}
