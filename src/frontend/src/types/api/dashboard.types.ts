export interface ResumenDashboard {
  ventas_hoy: number;
  total_facturado_hoy: number;
  productos_stock_bajo: number;
}

export interface ProductoStockBajo {
  producto_id: string;
  codigo: string;
  nombre: string;
  stock_actual: number;
}
