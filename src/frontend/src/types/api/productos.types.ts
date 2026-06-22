import type { StockProducto } from '@/types/domain';

/**
 * Response de GET /api/v1/productos/buscar?query=...
 *
 * ⚠️ Alineado con el endpoint oficial documentado:
 * GET /api/v1/productos/buscar?query=...
 *
 * Nota: Los nombres de campos en snake_case reflejan los esquemas Pydantic
 * del backend. El mapper toStockProducto() los convierte a camelCase del dominio.
 */
export interface ProductoBusquedaResponse {
  productos: ProductoBusquedaItem[];
  total: number;
}

export interface ProductoBusquedaItem {
  codigo: string;
  nombre: string;
  categoria: string;
  stock_actual: number;
  stock_minimo: number;
  actualizado_en: string; // ISO 8601
}

/**
 * Query params de GET /api/v1/productos/buscar
 *
 * ⚠️ El parámetro oficial es `query` (no `q`).
 * Ver tabla oficial de endpoints en FE-Architect-Scaffold.md.
 */
export interface ProductoBusquedaParams {
  query: string;
}

/**
 * Mapper: API (snake_case) → Domain (camelCase)
 *
 * SRP: Única función responsable del mapeo de la respuesta de búsqueda.
 */
export function toStockProducto(item: ProductoBusquedaItem): StockProducto {
  return {
    codigo: item.codigo,
    nombre: item.nombre,
    stockActual: item.stock_actual,
    stockMinimo: item.stock_minimo,
    disponible: item.stock_actual > 0,
    bajoStock: item.stock_actual > 0 && item.stock_actual < item.stock_minimo,
  };
}