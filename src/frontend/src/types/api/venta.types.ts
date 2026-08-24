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
 * Ítem de la compra original mostrado al validar un ticket (HU-04).
 * Espejo del esquema Pydantic ItemTicketResponse.
 */
export interface ItemTicketResponse {
  producto_id: string;
  nombre: string;
  cantidad: number;
  precio: number;
}

/**
 * Response de GET /api/v1/ventas/validar-ticket/{numero_ticket} (HU-04).
 * Espejo del esquema Pydantic ValidarTicketResponse.
 */
export interface ValidarTicketResponse {
  existe: true;
  /** ID de la venta original, requerido para registrar el cambio (HU-02) */
  venta_original_id: string;
  numero_ticket: string;
  fecha_compra: string;
  cajero_original_id: string;
  items: ItemTicketResponse[];
  mensaje: string;
}

/**
 * Error 404 de GET /api/v1/ventas/validar-ticket/{numero_ticket} (HU-04).
 * Espejo del esquema Pydantic TicketNoEncontradoErrorResponse.
 */
export interface TicketNoEncontradoErrorResponse {
  existe: false;
  error: string;
  mensaje: string;
}

/**
 * Response de PATCH /api/v1/ventas/{numero_ticket}/estado (HU-04).
 * Espejo del esquema Pydantic MarcarEnCambioResponse.
 */
export interface MarcarEnCambioResponse {
  numero_ticket: string;
  estado: string;
  mensaje: string;
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