import type { StockProducto } from '@/types/domain';

/**
 * Response de GET /api/v1/productos/stock
 * Espejo del esquema Pydantic StockSearchResponse del backend.
 */
export interface StockResponse {
  producto_id: string;
  nombre: string;
  stock_actual: number;
}

export interface StockSearchResponse {
  productos: StockResponse[];
  mensaje: string;
}

/**
 * Mapper: API → Domain
 */
export function toStockProducto(response: StockResponse): StockProducto {
  return {
    codigo: response.producto_id,
    nombre: response.nombre,
    stockActual: response.stock_actual,
    stockMinimo: 0,
    disponible: response.stock_actual > 0,
    bajoStock: response.stock_actual <= 0,
  };
}