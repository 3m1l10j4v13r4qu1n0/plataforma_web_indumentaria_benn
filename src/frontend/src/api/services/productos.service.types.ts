import type { StockProducto, ProductoBusqueda } from '@/types/domain';

/**
 * Contrato del servicio de productos.
 * SRP: solo operaciones de consulta de productos y stock.
 */
export interface IProductosService {
  /**
   * Consulta el stock de un producto por su código.
   * Lanza 404 si el producto no existe.
   */
  obtenerStock(codigo: string): Promise<StockProducto>;

  /**
   * Busca productos por nombre o código y devuelve su stock.
   * Lanza 400 si el query tiene menos de 3 caracteres.
   */
  buscarProductos(query: string): Promise<{
    resultados: ProductoBusqueda[];
    totalEncontrados: number;
    mensaje?: string | null;
  }>;
}