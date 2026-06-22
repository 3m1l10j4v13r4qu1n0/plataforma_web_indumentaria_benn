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
 * Proyección específica para la HU-06 (Consulta de stock).
 *
 * ⚠️ Alineado con el endpoint oficial:
 * GET /api/v1/productos/buscar?query=...
 */
export interface StockProducto {
  codigo: string;
  nombre: string;
  categoria?: string; // Opcional: el backend puede no devolverlo siempre
  stockActual: number;
  stockMinimo: number;
  disponible: boolean;
  bajoStock: boolean;
  actualizadoEn?: string; // ISO 8601 — opcional según respuesta del backend
}