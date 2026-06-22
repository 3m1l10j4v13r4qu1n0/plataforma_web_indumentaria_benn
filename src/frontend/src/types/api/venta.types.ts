/**
 * Item del carrito de ventas.
 * Representa un producto agregado a la venta actual.
 */
export interface ItemCarrito {
  productoId: string;
  codigo: string;
  nombre: string;
  categoria: string;
  precio: number;
  stockActual: number;
  cantidad: number;
}

/**
 * Venta procesada (respuesta del backend).
 */
export interface VentaProcesada {
  id: string;
  numeroTicket: string;
  fechaHora: string;
  vendedorId: string;
  estado: string;
  items: ItemVentaResponse[];
  descuento: DescuentoResponse;
}

export interface ItemVentaResponse {
  productoId: string;
  cantidad: number;
}

export interface DescuentoResponse {
  porcentaje: number;
  gerenteAutorizacionId?: string;
}

/**
 * Resultado de validación del carrito.
 */
export interface ValidacionCarrito {
  esValido: boolean;
  errores: ErrorValidacionItem[];
}

export interface ErrorValidacionItem {
  productoId: string;
  nombre: string;
  motivo: 'SIN_STOCK' | 'CANTIDAD_EXCEDE_STOCK' | 'CANTIDAD_CERO';
  mensaje: string;
}
