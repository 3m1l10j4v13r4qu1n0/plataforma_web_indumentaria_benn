/**
 * Item individual dentro de un ticket de venta.
 */
export interface ItemTicket {
  productoId: string;
  nombre: string;
  cantidad: number;
  precioUnitario: number;
  subtotal: number;
}

/**
 * Ticket de venta completo para visualización e impresión.
 */
export interface Ticket {
  numeroTicket: string;
  fechaHora: string; // ISO 8601
  vendedorId: string;
  estado: string;
  items: ItemTicket[];
  totalArticulos: number;
  totalPagar: number;
}

/**
 * Estados posibles de la impresora (Simulación para HU-07).
 */
export type EstadoImpresora = 'idle' | 'printing' | 'success' | 'error';
