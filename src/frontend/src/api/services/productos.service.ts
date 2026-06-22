import { apiClient } from '@/api/client';
import { API_ENDPOINTS } from '@/api/endpoints';
import type {
  ProductoBusquedaParams,
  ProductoBusquedaResponse,
  StockResponse,
} from '@/types/api';

/**
 * Servicio HTTP para operaciones de productos.
 */
export const productosService = {
  /**
   * Busca productos por nombre o código.
   * Endpoint: GET /api/v1/productos/buscar?query=...
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

  /**
   * Consulta el stock de un producto por su código.
   * Endpoint: GET /api/v1/productos/{codigo}/stock
   * HU asociada: HU-01
   *
   * @throws {AxiosError} con código 404 si el producto no existe
   */
  async obtenerStock(codigo: string): Promise<StockResponse> {
    const response = await apiClient.get<StockResponse>(
      API_ENDPOINTS.PRODUCTOS.STOCK(codigo),
    );
    return response.data;
  },
};
