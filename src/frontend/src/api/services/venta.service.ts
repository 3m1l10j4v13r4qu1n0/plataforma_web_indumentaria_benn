import { apiClient } from '@/api/client';
import { API_ENDPOINTS } from '@/api/endpoints';
import type { CrearVentaRequest, VentaResponse } from '@/types/api';

/**
 * Servicio HTTP para operaciones de venta.
 *
 * SRP: Única capa que conoce los endpoints del backend para el dominio de ventas.
 *
 * ⚠️ Anti-alucinación: Solo consume endpoints de la lista oficial.
 */
export const ventaService = {
  /**
   * Procesa una venta (valida stock y descuenta inventario).
   * Endpoint: POST /api/v1/ventas
   * HU asociada: HU-01
   *
   * @throws {AxiosError} con código 409 si hay STOCK_INSUFICIENTE
   */
  async procesarVenta(request: CrearVentaRequest): Promise<VentaResponse> {
    const response = await apiClient.post<VentaResponse>(
      API_ENDPOINTS.VENTAS.CREATE,
      request,
    );
    return response.data;
  },
};
