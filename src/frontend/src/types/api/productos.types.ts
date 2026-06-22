import type { StockProducto } from '@/types/domain';

/**
 * Response de GET /api/v1/productos/buscar?query=...
 *
 * ⚠️ Alineado con el endpoint oficial documentado.
 * Los campos en snake_case reflejan los esquemas Pydantic del backend.
 */
export interface ProductoBusquedaResponse {
  productos: ProductoBusquedaItem[];
  total: number;
}

export interface ProductoBusquedaItem {
  codigo: string;
  nombre: string;
  categoria?: string;
  stock_actual: number;
  stock_minimo: number;
  actualizado_en?: string; // ISO 8601
}

export interface ProductoBusquedaParams {
  query: string;
}

/**
 * Mapper: API (snake_case) → Domain (camelCase)
 * SRP: Única función responsable del mapeo de la respuesta de búsqueda.
 */
export function toStockProducto(item: ProductoBusquedaItem): StockProducto {
  return {
    codigo: item.codigo,
    nombre: item.nombre,
    categoria: item.categoria,
    stockActual: item.stock_actual,
    stockMinimo: item.stock_minimo,
    disponible: item.stock_actual > 0,
    bajoStock: item.stock_actual > 0 && item.stock_actual < item.stock_minimo,
    actualizadoEn: item.actualizado_en,
  };
}