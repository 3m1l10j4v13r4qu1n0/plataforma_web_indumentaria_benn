import type { StockProducto, ProductoBusqueda } from '@/types/domain';

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
 * Mapper: API → Domain (Stock)
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

/**
 * Elemento individual de la respuesta de búsqueda.
 * Espejo EXACTO del esquema Pydantic ProductoStockResponse del backend.
 */
export interface ProductoBusquedaResponse {
  producto_id: string;
  codigo: string;
  nombre: string;
  stock_actual: number;
  estado: string;
}

/**
 * Response de GET /api/v1/productos/buscar?query={termino}
 * Espejo EXACTO del esquema Pydantic BuscarProductosResponse del backend.
 */
export interface BuscarProductosResponse {
  resultados: ProductoBusquedaResponse[];
  total_encontrados: number;
  mensaje?: string | null;
}

/**
 * Mapper: API → Domain (Búsqueda de productos)
 */
export function toProductoBusqueda(
  response: ProductoBusquedaResponse,
): ProductoBusqueda {
  return {
    productoId: response.producto_id,
    codigo: response.codigo,
    nombre: response.nombre,
    stockActual: response.stock_actual,
    estado: response.estado,
  };
}