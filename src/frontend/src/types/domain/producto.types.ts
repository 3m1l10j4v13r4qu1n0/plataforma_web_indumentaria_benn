/**
 * Producto del catálogo.
 * Refleja el modelo de datos definido en modelo_datos_global.md.
 */
export interface Producto {
  id: string;
  codigo: string;
  nombre: string;
  descripcion: string;
  precio: number;
  categoria: string;
  stockActual: number;
  stockMinimo: number;
  permiteCambio: boolean;
  plazoCambioDias: number;
  activo: boolean;
  createdAt: string;
  updatedAt: string;
}

/**
 * Información de stock de un producto.
 * Espejo del StockResponse del backend (HU-01/HU-06).
 */
export interface StockProducto {
  productoId: string;
  categoria: string;
  nombre: string;
  precio: number;
  stockActual: number;
}

/**
 * Producto resultante de una búsqueda (HU-06).
 * Espejo del ProductoStockResponse del backend.
 */
export interface ProductoBusqueda {
  productoId: string;
  codigo: string;
  nombre: string;
  stockActual: number;
  estado: string;
}