import { apiClient } from '@/api/client';
import { API_ENDPOINTS } from '@/api/endpoints';
import type { StockSearchResponse } from '@/types/api/productos.types';

class ProductosService {
  async buscarStock(query: string): Promise<StockSearchResponse> {
    const response = await apiClient.get<StockSearchResponse>(
      API_ENDPOINTS.PRODUCTOS.STOCK,
      {
        params: { query },
      },
    );

    return response.data;
  }
}

export const productosService = new ProductosService();
