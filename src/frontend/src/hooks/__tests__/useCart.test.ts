import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useCart } from '@/hooks/useCart';
import type { ProductoBusquedaItem } from '@/types/api';

const mockProducto: ProductoBusquedaItem = {
  producto_id: 'P-001',
  codigo: 'CAM-001',
  nombre: 'Camiseta Básica',
  precio: 25.0,
  categoria: 'Indumentaria',
  stock_actual: 5,
  estado: 'ACTIVO',
};

describe('useCart', () => {
  it('inicializa con carrito vacío', () => {
    const { result } = renderHook(() => useCart());

    expect(result.current.items).toEqual([]);
    expect(result.current.totalArticulos).toBe(0);
    expect(result.current.totalPagar).toBe(0);
    expect(result.current.isEmpty).toBe(true);
  });

  it('agrega un producto al carrito con cantidad 1', () => {
    const { result } = renderHook(() => useCart());

    act(() => {
      result.current.addProduct(mockProducto);
    });

    expect(result.current.items).toHaveLength(1);
    expect(result.current.items[0]).toMatchObject({
      productoId: 'P-001',
      nombre: 'Camiseta Básica',
      precio: 25.0,
      stockActual: 5,
      cantidad: 1,
    });
    expect(result.current.totalArticulos).toBe(1);
    expect(result.current.totalPagar).toBe(25.0);
    expect(result.current.isEmpty).toBe(false);
  });

  it('incrementa la cantidad si el producto ya existe', () => {
    const { result } = renderHook(() => useCart());

    act(() => {
      result.current.addProduct(mockProducto);
      result.current.addProduct(mockProducto);
    });

    expect(result.current.items).toHaveLength(1);
    expect(result.current.items[0].cantidad).toBe(2);
    expect(result.current.totalPagar).toBe(50.0);
  });

  it('no permite que la cantidad supere el stock disponible', () => {
    const { result } = renderHook(() => useCart());

    act(() => {
      // Stock es 5, agregamos 6 veces
      for (let i = 0; i < 6; i++) {
        result.current.addProduct(mockProducto);
      }
    });

    expect(result.current.items[0].cantidad).toBe(5); // Máximo = stock
  });

  it('actualiza la cantidad de un producto', () => {
    const { result } = renderHook(() => useCart());

    act(() => {
      result.current.addProduct(mockProducto);
      result.current.updateQuantity('P-001', 3);
    });

    expect(result.current.items[0].cantidad).toBe(3);
    expect(result.current.totalPagar).toBe(75.0);
  });

  it('remueve el producto si la cantidad se establece en 0', () => {
    const { result } = renderHook(() => useCart());

    act(() => {
      result.current.addProduct(mockProducto);
      result.current.updateQuantity('P-001', 0);
    });

    expect(result.current.items).toHaveLength(0);
    expect(result.current.isEmpty).toBe(true);
  });

  it('remueve un producto específico', () => {
    const { result } = renderHook(() => useCart());

    act(() => {
      result.current.addProduct(mockProducto);
      result.current.removeProduct('P-001');
    });

    expect(result.current.items).toHaveLength(0);
  });

  it('limpia todo el carrito', () => {
    const { result } = renderHook(() => useCart());

    act(() => {
      result.current.addProduct(mockProducto);
      result.current.addProduct({ ...mockProducto, producto_id: 'P-002', codigo: 'PAN-042' });
      result.current.clearCart();
    });

    expect(result.current.items).toEqual([]);
    expect(result.current.isEmpty).toBe(true);
  });

  it('calcula correctamente el total con múltiples productos', () => {
    const { result } = renderHook(() => useCart());

    act(() => {
      result.current.addProduct(mockProducto); // 25.0 x 1
      result.current.addProduct({
        ...mockProducto,
        producto_id: 'P-002',
        codigo: 'PAN-042',
        nombre: 'Pantalón',
        precio: 40.0,
      }); // 40.0 x 1
      result.current.updateQuantity('P-002', 2); // 40.0 x 2
    });

    expect(result.current.totalArticulos).toBe(3); // 1 + 2
    expect(result.current.totalPagar).toBe(105.0); // 25 + 80
  });
});
