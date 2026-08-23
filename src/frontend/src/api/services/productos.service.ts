import { apiClient } from '@/api/client';
import { API_ENDPOINTS } from '@/api/endpoints';
import type { StockProducto } from '@/types/domain';
import {
  StockResponse,
  BuscarProductosResponse,
  toStockProducto,
  toProductoBusqueda,
} from '@/types/api';

import type { IProductosService } from './productos.service.types';

/**
 * Implementación concreta del servicio de productos usando el cliente Axios.
 */
export const productosService: IProductosService = {
  async obtenerStock(codigo: string): Promise<StockProducto> {
    const { data } = await apiClient.get<StockResponse>(
      API_ENDPOINTS.PRODUCTOS.STOCK(codigo),
    );
    return toStockProducto(data);
  },

  async buscarProductos(query: string) {
    const { data } = await apiClient.get<BuscarProductosResponse>(
      API_ENDPOINTS.PRODUCTOS.BUSCAR(query),
    );
    return {
      resultados: data.resultados.map(toProductoBusqueda),
      totalEncontrados: data.total_encontrados,
      mensaje: data.mensaje,
    };
  },
};