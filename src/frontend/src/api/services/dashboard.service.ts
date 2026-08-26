import { apiClient } from '@/api/client';
import { API_ENDPOINTS } from '@/api/endpoints';
import type { ResumenDashboard, ProductoStockBajo } from '@/types/api/dashboard.types';

export const dashboardService = {
  async obtenerResumen(): Promise<ResumenDashboard> {
    const { data } = await apiClient.get<ResumenDashboard>(
      API_ENDPOINTS.DASHBOARD.RESUMEN,
    );
    return data;
  },

  async obtenerProductosStockBajo(): Promise<ProductoStockBajo[]> {
    const { data } = await apiClient.get<ProductoStockBajo[]>(
      API_ENDPOINTS.DASHBOARD.PRODUCTOS_STOCK_BAJO,
    );
    return data;
  },
};
