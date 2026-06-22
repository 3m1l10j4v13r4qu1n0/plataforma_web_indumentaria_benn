import type { StockProducto } from '@/types/domain';
import type { ProductoSearchParams, ProductoItem } from '@/types/api';

/**
 * Contrato del servicio de productos.
 * SRP: solo operaciones de consulta de productos/stock.
 */
export interface IProductosService {
  /**
   * Consulta el stock de un producto por su código.
   * @throws {ProductoError} si el producto no existe o hay error de validación.
   */
  obtenerStock(codigo: string): Promise<StockProducto>;

  /**
   * Busca productos con filtros opcionales.
   */
  buscarProductos(params?: ProductoSearchParams): Promise<ProductoItem[]>;
}