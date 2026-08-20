import type { StockProducto } from '@/types/domain';

/**
 * Response de GET /api/v1/productos/{codigo}/stock
 * Espejo del esquema Pydantic StockResponse del backend.
 */
export interface StockResponse {
  producto_id: string;
  categoria: string;
  nombre: string;
  precio: number;
  stock_actual: number;
}

/**
 * Mapper: API → Domain
 */
export function toStockProducto(response: StockResponse): StockProducto {
  return {
    productoId: response.producto_id,
    categoria: response.categoria,
    nombre: response.nombre,
    precio: response.precio,
    stockActual: response.stock_actual,
  };
}