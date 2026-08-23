import { apiClient } from '@/api/client';
import { API_ENDPOINTS } from '@/api/endpoints';
import type { AplicarDescuentoRequest, DescuentoResponse } from '@/types/api';

/**
 * Contrato del servicio de descuentos.
 * SRP: solo operaciones de aplicación de descuentos.
 */
export interface IDescuentoService {
  /**
   * Aplica un descuento a una venta existente.
   * @throws {AxiosError} si el descuento supera el límite sin autorización (422).
   */
  aplicarDescuento(request: AplicarDescuentoRequest): Promise<DescuentoResponse>;
}

/**
 * Implementación concreta del servicio de descuentos usando el cliente Axios.
 */
export const descuentoService: IDescuentoService = {
  async aplicarDescuento(request: AplicarDescuentoRequest): Promise<DescuentoResponse> {
    const { data } = await apiClient.post(API_ENDPOINTS.DESCUENTOS.APPLY, request);
    return data;
  },
};
