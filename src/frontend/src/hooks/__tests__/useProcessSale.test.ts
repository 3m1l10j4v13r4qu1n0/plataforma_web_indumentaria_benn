import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor, act } from '@testing-library/react';
import { useProcessSale } from '@/hooks/useProcessSale';
import { ventaService } from '@/api/services/venta.service';
import { AllProviders } from '@/test/test-utils';
import type { ItemCarrito } from '@/types/domain';
import type { VentaResponse } from '@/types/api';
import axios from 'axios';

vi.mock('@/api/services/venta.service', () => ({
  ventaService: {
    procesarVenta: vi.fn(),
  },
}));

const mockedService = vi.mocked(ventaService);

const mockCarrito: ItemCarrito[] = [
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

const mockVentaResponse: VentaResponse = {
  id: 'venta-123',
  numero_ticket: 'TK-20260622-001',
  fecha_hora: '2026-06-22T14:30:00Z',
  vendedor_id: 'V-001',
  estado: 'COMPLETADA',
  items: [{ producto_id: 'P-001', cantidad: 2 }],
  descuento: { porcentaje: 0.0 },
};

describe('useProcessSale', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('procesa la venta exitosamente y devuelve ventaProcesada', async () => {
    mockedService.procesarVenta.mockResolvedValueOnce(mockVentaResponse);

    const { result } = renderHook(() => useProcessSale(), {
      wrapper: AllProviders,
    });

    act(() => {
      result.current.processSale(mockCarrito, 'V-001');
    });

    expect(result.current.isProcessing).toBe(true);

    await waitFor(() => {
      expect(result.current.isProcessing).toBe(false);
    });

    expect(result.current.ventaProcesada).toMatchObject({
      numeroTicket: 'TK-20260622-001',
      vendedorId: 'V-001',
    });
    expect(result.current.error).toBeNull();
  });

  it('llama al servicio con el formato correcto (snake_case)', async () => {
    mockedService.procesarVenta.mockResolvedValueOnce(mockVentaResponse);

    const { result } = renderHook(() => useProcessSale(), {
      wrapper: AllProviders,
    });

    act(() => {
      result.current.processSale(mockCarrito, 'V-001');
    });

    await waitFor(() => {
      expect(mockedService.procesarVenta).toHaveBeenCalledWith({
        vendedor_id: 'V-001',
        items: [{ producto_id: 'P-001', cantidad: 2 }],
        porcentaje_descuento: 0.0,
        gerente_autorizacion_id: undefined,
      });
    });
  });

  it('expone error estructurado cuando el backend devuelve STOCK_INSUFICIENTE', async () => {
    const axiosError = Object.assign(
      new Error('Request failed'),
      {
        isAxiosError: true,
        response: {
          status: 409,
          data: {
            error: 'STOCK_INSUFICIENTE',
            mensaje: "El producto 'Camiseta' no tiene stock disponible.",
            producto_id: 'P-001',
          },
        },
      },
    );

    // Mockear axios.isAxiosError
    vi.spyOn(axios, 'isAxiosError').mockReturnValue(true);
    mockedService.procesarVenta.mockRejectedValueOnce(axiosError);

    const { result } = renderHook(() => useProcessSale(), {
      wrapper: AllProviders,
    });

    act(() => {
      result.current.processSale(mockCarrito, 'V-001');
    });

    await waitFor(() => {
      expect(result.current.isProcessing).toBe(false);
    });

    expect(result.current.error).toEqual({
      code: 'STOCK_INSUFICIENTE',
      message: "El producto 'Camiseta' no tiene stock disponible.",
    });
    expect(result.current.ventaProcesada).toBeNull();
  });

  it('permite resetear el estado después de un error', async () => {
    mockedService.procesarVenta.mockRejectedValueOnce(new Error('Network Error'));

    const { result } = renderHook(() => useProcessSale(), {
      wrapper: AllProviders,
    });

    act(() => {
      result.current.processSale(mockCarrito, 'V-001');
    });

    await waitFor(() => {
      expect(result.current.error).not.toBeNull();
    });

    act(() => {
      result.current.reset();
    });

    expect(result.current.error).toBeNull();
    expect(result.current.ventaProcesada).toBeNull();
  });
});
