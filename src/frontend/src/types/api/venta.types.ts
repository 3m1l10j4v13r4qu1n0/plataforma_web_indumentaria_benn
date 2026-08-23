/**
 * Item de venta en la request de POST /api/v1/ventas.
 * Espejo del esquema Pydantic ItemVentaRequest.
 */
export interface ItemVentaRequest {
  producto_id: string;
  cantidad: number;
}

/**
 * Request de POST /api/v1/ventas.
 * Espejo del esquema Pydantic CrearVentaRequest.
 */
export interface CrearVentaRequest {
  vendedor_id: string;
  items: ItemVentaRequest[];
}

/**
 * Item de venta en la respuesta de POST /api/v1/ventas.
 * Espejo del esquema Pydantic ItemVentaResponse.
 */
export interface ItemVentaResponse {
  producto_id: string;
  nombre: string;
  cantidad: number;
  precio: number;
}

/**
 * Response de POST /api/v1/ventas.
 * Espejo del esquema Pydantic VentaResponse.
 */
export interface VentaResponse {
  id: string;
  fecha_hora: string;
  vendedor_id: string;
  estado: string;
  numero_ticket: string | null;
  total: number | null;
  mensaje: string | null;
  items: ItemVentaResponse[];
}