import { apiClient } from '@/api/client';
import { API_ENDPOINTS } from '@/api/endpoints';
import type {
  ProductoBusquedaParams,
  ProductoBusquedaResponse,
} from '@/types/api';

/**
 * Servicio HTTP para operaciones de productos.
 *
 * SRP: Única capa que conoce los endpoints y formatos del backend
 *      para el dominio de productos.
 * DIP: Expone funciones tipadas; los hooks dependen de estas, no de Axios.
 *
 * ⚠️ Anti-alucinación: Solo consume endpoints de la lista oficial.
 */
export const productosService = {
  /**
   * Busca productos por nombre o código.
   * Endpoint: GET /api/v1/productos/buscar?query=...
   * HU asociada: HU-06
   *
   * @throws {AxiosError} si la petición falla (manejado por interceptor global)
   */
  async buscarProductos(
    params: ProductoBusquedaParams,
  ): Promise<ProductoBusquedaResponse> {
    const response = await apiClient.get<ProductoBusquedaResponse>(
      API_ENDPOINTS.PRODUCTOS.BUSCAR,
      { params },
    );
    return response.data;
  },
};