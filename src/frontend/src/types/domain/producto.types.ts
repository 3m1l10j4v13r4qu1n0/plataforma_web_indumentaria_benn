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
 * Proyección específica para la HU-06.
 */
export interface StockProducto {
  codigo: string;
  nombre: string;
  stockActual: number;
  stockMinimo: number;
  disponible: boolean;
  bajoStock: boolean;
}