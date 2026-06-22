import { describe, it, expect } from 'vitest';
import { toStockProducto } from '@/types/api';
import type { ProductoBusquedaItem } from '@/types/api';

describe('toStockProducto (mapper API → Domain)', () => {
  it('mapea correctamente snake_case a camelCase', () => {
    const item: ProductoBusquedaItem = {
      codigo: 'CAM-001',
      nombre: 'Camiseta Básica Azul',
      categoria: 'Indumentaria',
      stock_actual: 24,
      stock_minimo: 5,
      actualizado_en: '2026-06-22T14:33:00Z',
    };

    const result = toStockProducto(item);

    expect(result).toEqual({
      codigo: 'CAM-001',
      nombre: 'Camiseta Básica Azul',
      categoria: 'Indumentaria',
      stockActual: 24,
      stockMinimo: 5,
      disponible: true,
      bajoStock: false,
      actualizadoEn: '2026-06-22T14:33:00Z',
    });
  });

  it('marca bajoStock=true cuando stock_actual < stock_minimo', () => {
    const item: ProductoBusquedaItem = {
      codigo: 'CAM-002',
      nombre: 'Camiseta Básica Roja',
      stock_actual: 2,
      stock_minimo: 5,
    };

    const result = toStockProducto(item);

    expect(result.bajoStock).toBe(true);
    expect(result.disponible).toBe(true);
  });

  it('marca disponible=false y bajoStock=false cuando stock es 0', () => {
    const item: ProductoBusquedaItem = {
      codigo: 'CAM-003',
      nombre: 'Camiseta Agotada',
      stock_actual: 0,
      stock_minimo: 5,
    };

    const result = toStockProducto(item);

    expect(result.disponible).toBe(false);
    expect(result.bajoStock).toBe(false);
  });

  it('maneja campos opcionales ausentes (categoria, actualizado_en)', () => {
    const item: ProductoBusquedaItem = {
      codigo: 'CAM-004',
      nombre: 'Producto Sin Categoría',
      stock_actual: 10,
      stock_minimo: 5,
    };

    const result = toStockProducto(item);

    expect(result.categoria).toBeUndefined();
    expect(result.actualizadoEn).toBeUndefined();
  });
});