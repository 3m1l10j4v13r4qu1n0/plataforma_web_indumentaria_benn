import type { ItemCarrito, Ticket, ItemTicket } from '@/types/domain';

/**
 * Response de GET /api/v1/ventas/tickets/{numero_ticket}
 * Espejo del esquema Pydantic TicketDetalleResponse.
 * 
 * ⚠️ NOTA: El backend NO devuelve precios ni totales en este endpoint.
 */
export interface TicketDetalleResponse {
  numero_ticket: string;
  fecha_hora: string;
  vendedor_id: string;
  estado: string;
  items: ItemTicketResponseApi[];
}

export interface ItemTicketResponseApi {
  producto_id: string;
  nombre: string;
  cantidad: number;
}

/**
 * Mapper: Construye un Ticket completo desde los datos locales del carrito
 * + la respuesta del backend (POST /api/v1/ventas).
 *
 * ⚠️ IMPORTANTE: Este mapper NO hace llamada HTTP. Usa datos que ya están
 * en memoria del frontend (carrito + respuesta de la venta procesada).
 *
 * SRP: Única función responsable de construir el Ticket para visualización.
 */
export function toTicket(params: {
  carrito: ItemCarrito[];
  numeroTicket: string;
  fechaHora: string;
  vendedorId: string;
  estado: string;
  totalArticulos: number;
  totalPagar: number;
}): Ticket {
  const items: ItemTicket[] = params.carrito.map((item) => ({
    productoId: item.productoId,
    nombre: item.nombre,
    cantidad: item.cantidad,
    precioUnitario: item.precio,
    subtotal: item.precio * item.cantidad,
  }));

  return {
    numeroTicket: params.numeroTicket,
    fechaHora: params.fechaHora,
    vendedorId: params.vendedorId,
    estado: params.estado,
    items,
    totalArticulos: params.totalArticulos,
    totalPagar: params.totalPagar,
  };
}
