import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useBuscarProductos } from '@/hooks/useBuscarProductos';
import { productosService } from '@/api/services/productos.service';
import { createTestQueryClient, AllProviders } from '@/test/test-utils';
import type { ProductoBusquedaResponse } from '@/types/api';

// Mock del servicio HTTP (SRP: aislamos el hook del backend real)
vi.mock('@/api/services/productos.service', () => ({
  productosService: {
    buscarProductos: vi.fn(),
  },
}));

const mockedService = vi.mocked(productosService);

const mockResponse: ProductoBusquedaResponse = {
  productos: [
    {
      codigo: 'CAM-001',
      nombre: 'Camiseta Azul',
      categoria: 'Indumentaria',
      stock_actual: 24,
      stock_minimo: 5,
      actualizado_en: '2026-06-22T14:33:00Z',
    },
  ],
  total: 1,
};

describe('useBuscarProductos', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('NO ejecuta la búsqueda si el query está vacío (enabled: false)', () => {
    renderHook(() => useBuscarProductos(''), {
      wrapper: AllProviders,
    });

    expect(mockedService.buscarProductos).not.toHaveBeenCalled();
  });

  it('NO ejecuta la búsqueda si el query son solo espacios', () => {
    renderHook(() => useBuscarProductos('   '), {
      wrapper: AllProviders,
    });

    expect(mockedService.buscarProductos).not.toHaveBeenCalled();
  });

  it('ejecuta la búsqueda y devuelve productos mapeados al dominio', async () => {
    mockedService.buscarProductos.mockResolvedValueOnce(mockResponse);

    const { result } = renderHook(() => useBuscarProductos('camiseta'), {
      wrapper: AllProviders,
    });

    // Estado inicial: loading
    expect(result.current.isLoading).toBe(true);
    expect(result.current.hasSearched).toBe(true);

    // Espera a que se resuelva
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.productos).toHaveLength(1);
    expect(result.current.productos[0]).toMatchObject({
      codigo: 'CAM-001',
      nombre: 'Camiseta Azul',
      stockActual: 24,
      disponible: true,
    });
    expect(result.current.total).toBe(1);
    expect(result.current.error).toBeNull();
  });

  it('devuelve array vacío y hasSearched=true cuando no hay resultados', async () => {
    mockedService.buscarProductos.mockResolvedValueOnce({
      productos: [],
      total: 0,
    });

    const { result } = renderHook(() => useBuscarProductos('xyz'), {
      wrapper: AllProviders,
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.productos).toEqual([]);
    expect(result.current.total).toBe(0);
  });

  it('expone el error cuando el servicio falla', async () => {
    const error = new Error('Network Error');
    mockedService.buscarProductos.mockRejectedValueOnce(error);

    const { result } = renderHook(() => useBuscarProductos('camiseta'), {
      wrapper: AllProviders,
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.error).toBeInstanceOf(Error);
    expect(result.current.error?.message).toBe('Network Error');
    expect(result.current.productos).toEqual([]);
  });

  it('llama al servicio con el parámetro query correcto', async () => {
    mockedService.buscarProductos.mockResolvedValueOnce(mockResponse);

    renderHook(() => useBuscarProductos('camiseta'), {
      wrapper: AllProviders,
    });

    await waitFor(() => {
      expect(mockedService.buscarProductos).toHaveBeenCalledWith({
        query: 'camiseta',
      });
    });
  });
});