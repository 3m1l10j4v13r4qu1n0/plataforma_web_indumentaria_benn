/**
 * Response de GET /api/v1/ventas/tickets/{numero_ticket}
 * Espejo del esquema Pydantic TicketDetalleResponse.
 * 
 * ⚠️ NOTA: El backend NO devuelve precios ni totales en este endpoint.
 */
export interface TicketDetalleResponse {
  numero_ticket: string;
  fecha_hora: string;
  vendedor_id: str;
  estado: string;
  items: ItemTicketResponseApi[];
}

export interface ItemTicketResponseApi {
  producto_id: string;
  nombre: string;
  cantidad: number;
}
