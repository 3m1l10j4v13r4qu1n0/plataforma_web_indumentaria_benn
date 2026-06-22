import type { StockProducto } from '@/types/domain';

/**
 * Response de GET /api/v1/productos/{codigo}/stock
 * Espejo del esquema Pydantic StockResponse del backend.
 */
export interface StockResponse {
  codigo: string;
  nombre: string;
  stock_actual: number;
  stock_minimo: number;
  disponible: boolean;
  bajo_stock: boolean;
}

/**
 * Response de GET /api/v1/productos/buscar
 * Espejo del esquema Pydantic ProductoSearchResponse del backend.
 */
export interface ProductoSearchResponse {
  productos: ProductoItem[];
  total: number;
  pagina: number;
  por_pagina: number;
}

export interface ProductoItem {
  id: string;
  codigo: string;
  nombre: string;
  precio: number;
  stock_actual: number;
  disponible: boolean;
}

/**
 * Query params de GET /api/v1/productos/buscar
 */
export interface ProductoSearchParams {
  q?: string;
  categoria?: string;
  pagina?: number;
  por_pagina?: number;
}

/**
 * Mapper: API → Domain
 */
export function toStockProducto(response: StockResponse): StockProducto {
  return {
    codigo: response.codigo,
    nombre: response.nombre,
    stockActual: response.stock_actual,
    stockMinimo: response.stock_minimo,
    disponible: response.disponible,
    bajoStock: response.bajo_stock,
  };
}