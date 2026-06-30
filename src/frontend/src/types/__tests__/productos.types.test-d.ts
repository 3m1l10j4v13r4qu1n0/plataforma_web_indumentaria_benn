import { describe, it, expectTypeOf } from 'vitest';
import type { StockResponse } from '@/types/api';
import { toStockProducto } from '@/types/api';
import type { StockProducto } from '@/types/domain';

describe('Productos Types', () => {
  it('toStockProducto mapea correctamente snake_case a camelCase', () => {
    const response: StockResponse = {
      codigo: 'PROD-001',
      nombre: 'Producto Test',
      stock_actual: 10,
      stock_minimo: 5,
      disponible: true,
      bajo_stock: false,
    };

    const result = toStockProducto(response);

    expectTypeOf(result).toMatchTypeOf<StockProducto>();
    expectTypeOf(result.codigo).toBeString();
    expectTypeOf(result.stockActual).toBeNumber();
    expectTypeOf(result.bajoStock).toBeBoolean();
  });

  it('StockProducto tiene todos los campos requeridos', () => {
    const stock: StockProducto = {
      codigo: 'PROD-001',
      nombre: 'Producto Test',
      stockActual: 10,
      stockMinimo: 5,
      disponible: true,
      bajoStock: false,
    };

    expectTypeOf(stock).toHaveProperty('codigo');
    expectTypeOf(stock).toHaveProperty('stockActual');
    expectTypeOf(stock).toHaveProperty('bajoStock');
  });
});