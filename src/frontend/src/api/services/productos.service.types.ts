import type { StockProducto } from '@/types/domain';

/**
 * Contrato del servicio de productos.
 * SRP: solo operaciones de consulta de stock.
 */
export interface IProductosService {
  /**
   * Consulta el stock de un producto por su código.
   * Lanza 404 si el producto no existe.
   */
  obtenerStock(codigo: string): Promise<StockProducto>;
}