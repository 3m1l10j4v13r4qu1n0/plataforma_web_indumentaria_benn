import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useCartValidation } from '@/hooks/useCartValidation';
import type { ItemCarrito } from '@/types/domain';

describe('useCartValidation', () => {
  it('valida como válido un carrito con stock suficiente', () => {
    const items: ItemCarrito[] = [
      {
        productoId: 'P-001',
        codigo: 'CAM-001',
        nombre: 'Camiseta',
        categoria: 'Indumentaria',
        precio: 25.0,
        stockActual: 5,
        cantidad: 2,
      },
    ];

    const { result } = renderHook(() => useCartValidation(items));

    expect(result.current.validacion.esValido).toBe(true);
    expect(result.current.validacion.errores).toHaveLength(0);
    expect(result.current.esProcesable).toBe(true);
  });

  it('detecta producto SIN_STOCK (stock_actual = 0)', () => {
    const items: ItemCarrito[] = [
      {
        productoId: 'P-001',
        codigo: 'PAN-042',
        nombre: 'Pantalón',
        categoria: 'Indumentaria',
        precio: 40.0,
        stockActual: 0,
        cantidad: 1,
      },
    ];

    const { result } = renderHook(() => useCartValidation(items));

    expect(result.current.validacion.esValido).toBe(false);
    expect(result.current.validacion.errores).toHaveLength(1);
    expect(result.current.validacion.errores[0]).toMatchObject({
      productoId: 'P-001',
      nombre: 'Pantalón',
      motivo: 'SIN_STOCK',
    });
    expect(result.current.esProcesable).toBe(false);
  });

  it('detecta CANTIDAD_EXCEDE_STOCK', () => {
    const items: ItemCarrito[] = [
      {
        productoId: 'P-001',
        codigo: 'ZAP-001',
        nombre: 'Zapatos',
        categoria: 'Calzado',
        precio: 80.0,
        stockActual: 2,
        cantidad: 3,
      },
    ];

    const { result } = renderHook(() => useCartValidation(items));

    expect(result.current.validacion.esValido).toBe(false);
    expect(result.current.validacion.errores[0].motivo).toBe('CANTIDAD_EXCEDE_STOCK');
    expect(result.current.esProcesable).toBe(false);
  });

  it('detecta CANTIDAD_CERO', () => {
    const items: ItemCarrito[] = [
      {
        productoId: 'P-001',
        codigo: 'CAM-001',
        nombre: 'Camiseta',
        categoria: 'Indumentaria',
        precio: 25.0,
        stockActual: 5,
        cantidad: 0,
      },
    ];

    const { result } = renderHook(() => useCartValidation(items));

    expect(result.current.validacion.esValido).toBe(false);
    expect(result.current.validacion.errores[0].motivo).toBe('CANTIDAD_CERO');
  });

  it('esProcesable es false si el carrito está vacío', () => {
    const { result } = renderHook(() => useCartValidation([]));

    expect(result.current.validacion.esValido).toBe(true); // Sin errores
    expect(result.current.esProcesable).toBe(false); // Pero vacío
  });

  it('valida múltiples productos con errores simultáneos', () => {
    const items: ItemCarrito[] = [
      {
        productoId: 'P-001',
        codigo: 'CAM-001',
        nombre: 'Camiseta',
        categoria: 'Indumentaria',
        precio: 25.0,
        stockActual: 5,
        cantidad: 2, // Válido
      },
      {
        productoId: 'P-002',
        codigo: 'PAN-042',
        nombre: 'Pantalón',
        categoria: 'Indumentaria',
        precio: 40.0,
        stockActual: 0,
        cantidad: 1, // SIN_STOCK
      },
      {
        productoId: 'P-003',
        codigo: 'ZAP-001',
        nombre: 'Zapatos',
        categoria: 'Calzado',
        precio: 80.0,
        stockActual: 2,
        cantidad: 5, // CANTIDAD_EXCEDE_STOCK
      },
    ];

    const { result } = renderHook(() => useCartValidation(items));

    expect(result.current.validacion.errores).toHaveLength(2);
    expect(result.current.esProcesable).toBe(false);
  });
});
