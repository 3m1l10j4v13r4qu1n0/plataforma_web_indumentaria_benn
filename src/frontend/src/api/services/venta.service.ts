import { apiClient } from '@/api/client';
import { API_ENDPOINTS } from '@/api/endpoints';
import type {
  CrearVentaRequest,
  MarcarEnCambioResponse,
  ValidarTicketResponse,
  VentaResponse,
} from '@/types/api';

/**
 * Contrato del servicio de ventas.
 * SRP: solo operaciones de procesamiento de ventas y tickets (HU-01, HU-04).
 */
export interface IVentaService {
  /**
   * Procesa una venta: valida stock y descuenta inventario en el backend.
   * @throws {VentaError} si hay stock insuficiente (409) o producto inválido (400).
   */
  procesarVenta(request: CrearVentaRequest): Promise<VentaResponse>;

  /**
   * Verifica la existencia de un ticket y devuelve los datos de la compra
   * original para iniciar el flujo de cambio (HU-04).
   * @throws error con código TICKET_NO_ENCONTRADO si no existe (404).
   */
  validarTicket(numeroTicket: string): Promise<ValidarTicketResponse>;

  /**
   * Retiene el ticket cambiando el estado de la venta a EN_CAMBIO (HU-04),
   * evitando que dos cajeros procesen el mismo ticket simultáneamente.
   * @throws VENTA_NO_ENCONTRADA (404) o VENTA_YA_EN_CAMBIO (409).
   */
  marcarVentaEnCambio(numeroTicket: string): Promise<MarcarEnCambioResponse>;
}

/**
 * Implementación concreta del servicio de ventas usando el cliente Axios.
 */
export const ventaService: IVentaService = {
  async procesarVenta(request: CrearVentaRequest): Promise<VentaResponse> {
    const { data } = await apiClient.post(API_ENDPOINTS.VENTAS.CREATE, request);
    return data;
  },

  async validarTicket(numeroTicket: string): Promise<ValidarTicketResponse> {
    const { data } = await apiClient.get(
      API_ENDPOINTS.VENTAS.VALIDAR_TICKET(numeroTicket),
    );
    return data;
  },

  async marcarVentaEnCambio(
    numeroTicket: string,
  ): Promise<MarcarEnCambioResponse> {
    const { data } = await apiClient.patch(
      API_ENDPOINTS.VENTAS.MARCAR_EN_CAMBIO(numeroTicket),
    );
    return data;
  },
};