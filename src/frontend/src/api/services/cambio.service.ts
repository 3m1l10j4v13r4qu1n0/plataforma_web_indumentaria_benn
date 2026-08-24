import { apiClient } from '@/api/client';
import { API_ENDPOINTS } from '@/api/endpoints';
import type {
  CambioResponse,
  ProcesarCambioRequest,
  ValidarEstadoProductoRequest,
  ValidarEstadoProductoResponse,
} from '@/types/api';

/**
 * Contrato del servicio de cambios.
 * SRP: solo operaciones del flujo de cambio de productos (HU-02, HU-03).
 */
export interface ICambioService {
  /**
   * Registra el cambio de un producto validando el plazo de 15 días (HU-02).
   * @throws PLAZO_VENCIDO (403) si pasaron más de 15 días desde la compra.
   */
  procesarCambio(request: ProcesarCambioRequest): Promise<CambioResponse>;

  /**
   * Valida el estado físico del producto presentado a cambio (HU-03).
   * Solo acepta productos NUEVO_ETIQUETADO con etiqueta.
   * @throws CAMBIO_NO_ENCONTRADO (404), PRODUCTO_NO_APTO (422)
   * u OBSERVACIONES_REQUERIDAS (422).
   */
  validarEstadoProducto(
    cambioId: string,
    request: ValidarEstadoProductoRequest,
  ): Promise<ValidarEstadoProductoResponse>;
}

/**
 * Implementación concreta del servicio de cambios usando el cliente Axios.
 */
export const cambioService: ICambioService = {
  async procesarCambio(request: ProcesarCambioRequest): Promise<CambioResponse> {
    const { data } = await apiClient.post(API_ENDPOINTS.CAMBIOS.CREATE, request);
    return data;
  },

  async validarEstadoProducto(
    cambioId: string,
    request: ValidarEstadoProductoRequest,
  ): Promise<ValidarEstadoProductoResponse> {
    const { data } = await apiClient.post(
      API_ENDPOINTS.CAMBIOS.VALIDAR_ESTADO(cambioId),
      request,
    );
    return data;
  },
};
