import { apiClient } from '@/api/client';
import { API_ENDPOINTS } from '@/api/endpoints';
import type { 
  CrearVentaRequest, 
  VentaResponse, 
  TicketDetalleResponse 
} from '@/types/api';

export const ventaService = {
  /**
   * Procesa una venta (valida stock y descuenta inventario).
   * Endpoint: POST /api/v1/ventas
   */
  async procesarVenta(request: CrearVentaRequest): Promise<VentaResponse> {
    const response = await apiClient.post<VentaResponse>(
      API_ENDPOINTS.VENTAS.CREATE,
      request,
    );
    return response.data;
  },

  /**
   * Obtiene el detalle de un ticket por su número.
   * Endpoint: GET /api/v1/ventas/tickets/{numero_ticket}
   * 
   * ⚠️ Nota: Este endpoint es usado principalmente por HU-04 (Cambios).
   * En HU-07 usamos los datos locales del carrito para la impresión inmediata.
   */
  async obtenerDetalleTicket(numeroTicket: string): Promise<TicketDetalleResponse> {
    const response = await apiClient.get<TicketDetalleResponse>(
      API_ENDPOINTS.VENTAS.TICKET(numeroTicket),
    );
    return response.data;
  },
};
