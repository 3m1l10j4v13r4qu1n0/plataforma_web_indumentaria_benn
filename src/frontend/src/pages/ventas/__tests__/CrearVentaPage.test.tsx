import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { CrearVentaPage } from '@/pages/ventas/CrearVentaPage';
import type { StockProducto } from '@/types/domain';
import type { VentaResponse } from '@/types/api';

vi.mock('@/api/services/productos.service', () => ({
  productosService: {
    obtenerStock: vi.fn(),
  },
}));

vi.mock('@/api/services/venta.service', () => ({
  ventaService: {
    procesarVenta: vi.fn(),
  },
}));

vi.mock('axios', () => {
  const clienteStub = () => ({
    get: vi.fn(),
    post: vi.fn(),
    interceptors: {
      request: { use: vi.fn() },
      response: { use: vi.fn() },
    },
  });
  return {
    default: {
      create: vi.fn(clienteStub),
      isAxiosError: (error: unknown) =>
        typeof error === 'object' &&
        error !== null &&
        'response' in error,
    },
  };
});

import { productosService } from '@/api/services/productos.service';
import { ventaService } from '@/api/services/venta.service';

const mockObtenerStock = vi.mocked(productosService.obtenerStock);
const mockProcesarVenta = vi.mocked(ventaService.procesarVenta);

const stockDisponible: StockProducto = {
  productoId: 'P-001',
  categoria: 'Remeras',
  nombre: 'Remera Azul',
  precio: 15000,
  stockActual: 10,
};

const stockCero: StockProducto = {
  ...stockDisponible,
  stockActual: 0,
};

const ventaOk: VentaResponse = {
  id: 'V-100',
  fecha_hora: '2026-08-19T12:00:00',
  vendedor_id: 'V-001',
  estado: 'CONFIRMADA',
  numero_ticket: 'T-20260819-001',
  total: 30000,
  mensaje: 'Venta registrada y ticket generado exitosamente.',
  items: [{ producto_id: 'P-001', nombre: 'Remera Azul', cantidad: 2, precio: 15000 }],
};

function renderizar() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <CrearVentaPage />
    </QueryClientProvider>,
  );
}

describe('CrearVentaPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('muestra el stock disponible al buscar un producto por código', async () => {
    const user = userEvent.setup();
    mockObtenerStock.mockResolvedValue(stockDisponible);
    renderizar();

    await user.type(screen.getByLabelText('Buscar producto por nombre o código'), 'P-001');
    await user.keyboard('{Enter}');

    expect(await screen.findByText('Remera Azul')).toBeInTheDocument();
    expect(
      await screen.findByLabelText('Stock: 10 unidades - 10 disponibles'),
    ).toBeInTheDocument();
    expect(mockObtenerStock).toHaveBeenCalledWith('P-001');
  });

  it('bloquea la venta cuando el producto no tiene stock', async () => {
    const user = userEvent.setup();
    mockObtenerStock.mockResolvedValue(stockCero);
    renderizar();

    await user.type(screen.getByLabelText('Buscar producto por nombre o código'), 'P-002');
    await user.keyboard('{Enter}');

    expect(await screen.findByRole('button', { name: 'Sin stock' })).toBeDisabled();
  });

  it('muestra el bloqueo preventivo cuando un ítem del carrito queda sin stock (E-01)', async () => {
    const user = userEvent.setup();
    mockObtenerStock
      .mockResolvedValueOnce(stockDisponible)
      .mockResolvedValueOnce(stockCero);
    renderizar();

    // Agregar el producto con stock disponible
    await user.type(screen.getByLabelText('Buscar producto por nombre o código'), 'P-001');
    await user.keyboard('{Enter}');
    await user.click(await screen.findByRole('button', { name: 'Agregar a venta' }));

    // Reconsultar: el backend ahora reporta stock 0 para ese producto
    await user.clear(screen.getByLabelText('Buscar producto por nombre o código'));
    await user.type(screen.getByLabelText('Buscar producto por nombre o código'), 'P-001');
    await user.keyboard('{Enter}');

    expect(
      await screen.findByText('No se puede procesar la venta'),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        'El producto "Remera Azul" no tiene stock disponible. Por favor, elimínalo del carrito para continuar.',
      ),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('button', { name: /Confirmar Venta/ }),
    ).toBeDisabled();
  });

  it('agrega un item, confirma la venta y muestra el éxito', async () => {
    const user = userEvent.setup();
    mockObtenerStock.mockResolvedValue(stockDisponible);
    mockProcesarVenta.mockResolvedValue(ventaOk);
    renderizar();

    // Buscar y agregar producto con cantidad 2
    await user.type(screen.getByLabelText('Buscar producto por nombre o código'), 'P-001');
    await user.keyboard('{Enter}');
    const cantidadInput = await screen.findByLabelText('Cantidad a vender');
    await user.clear(cantidadInput);
    await user.type(cantidadInput, '2');
    await user.click(screen.getByRole('button', { name: 'Agregar a venta' }));

    // Confirmar venta
    await user.click(screen.getByRole('button', { name: 'Confirmar Venta' }));

    expect(await screen.findByText('¡Venta Registrada!')).toBeInTheDocument();
    expect(screen.getByText('TIENDA RETAIL S.A.')).toBeInTheDocument();
    expect(screen.getByText('T-20260819-001')).toBeInTheDocument();
    expect(mockProcesarVenta).toHaveBeenCalledWith({
      vendedor_id: 'V-001',
      items: [{ producto_id: 'P-001', cantidad: 2 }],
    });
  });

  it('muestra el toast verde de éxito con el mensaje de HU-08', async () => {
    const user = userEvent.setup();
    mockObtenerStock.mockResolvedValue(stockDisponible);
    mockProcesarVenta.mockResolvedValue(ventaOk);
    renderizar();

    await user.type(screen.getByLabelText('Buscar producto por nombre o código'), 'P-001');
    await user.keyboard('{Enter}');
    await user.click(await screen.findByRole('button', { name: 'Agregar a venta' }));
    await user.click(screen.getByRole('button', { name: 'Confirmar Venta' }));

    expect(
      await screen.findByText('Venta registrada e inventario actualizado'),
    ).toBeInTheDocument();
  });

  it('muestra alerta de stock insuficiente cuando el backend rechaza la venta', async () => {
    const user = userEvent.setup();
    mockObtenerStock.mockResolvedValue(stockDisponible);
    const axiosError = {
      isAxiosError: true,
      response: {
        status: 409,
        data: {
          error: 'STOCK_INSUFICIENTE',
          mensaje: 'Stock insuficiente para P-001',
          producto_id: 'P-001',
        },
      },
    };
    mockProcesarVenta.mockRejectedValue(axiosError);
    renderizar();

    await user.type(screen.getByLabelText('Buscar producto por nombre o código'), 'P-001');
    await user.keyboard('{Enter}');
    await user.click(await screen.findByRole('button', { name: 'Agregar a venta' }));
    await user.click(screen.getByRole('button', { name: 'Confirmar Venta' }));

    expect(
      await screen.findByText('No hay stock suficiente para completar la venta.'),
    ).toBeInTheDocument();
  });
});