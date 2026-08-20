import { describe, it, expectTypeOf } from 'vitest';
import type { StockResponse } from '@/types/api';
import { toStockProducto } from '@/types/api';
import type { StockProducto } from '@/types/domain';

describe('Productos Types', () => {
  it('toStockProducto mapea correctamente snake_case a camelCase', () => {
    const response: StockResponse = {
      producto_id: 'PROD-001',
      categoria: 'Remeras',
      nombre: 'Producto Test',
      precio: 15000,
      stock_actual: 10,
    };

    const result = toStockProducto(response);

    expectTypeOf(result).toExtend<StockProducto>();
    expectTypeOf(result.productoId).toBeString();
    expectTypeOf(result.stockActual).toBeNumber();
    expectTypeOf(result.categoria).toBeString();
  });

  it('StockProducto tiene todos los campos requeridos', () => {
    const stock: StockProducto = {
      productoId: 'PROD-001',
      categoria: 'Remeras',
      nombre: 'Producto Test',
      precio: 15000,
      stockActual: 10,
    };

    expectTypeOf(stock).toHaveProperty('productoId');
    expectTypeOf(stock).toHaveProperty('stockActual');
    expectTypeOf(stock).toHaveProperty('categoria');
  });
});