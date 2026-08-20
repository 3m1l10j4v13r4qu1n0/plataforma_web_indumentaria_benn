import { apiClient } from '@/api/client';
import { API_ENDPOINTS } from '@/api/endpoints';
import type { CrearVentaRequest, VentaResponse } from '@/types/api';

/**
 * Contrato del servicio de ventas.
 * SRP: solo operaciones de procesamiento de ventas.
 */
export interface IVentaService {
  /**
   * Procesa una venta: valida stock y descuenta inventario en el backend.
   * @throws {VentaError} si hay stock insuficiente (409) o producto inválido (400).
   */
  procesarVenta(request: CrearVentaRequest): Promise<VentaResponse>;
}

/**
 * Implementación concreta del servicio de ventas usando el cliente Axios.
 */
export const ventaService: IVentaService = {
  async procesarVenta(request: CrearVentaRequest): Promise<VentaResponse> {
    const { data } = await apiClient.post(API_ENDPOINTS.VENTAS.CREATE, request);
    return data;
  },
};