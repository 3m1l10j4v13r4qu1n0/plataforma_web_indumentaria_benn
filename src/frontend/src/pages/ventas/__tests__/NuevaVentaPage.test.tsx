import { describe, it, expect, vi, beforeEach } from 'vitest';
import { screen, waitFor } from '@/test/test-utils';
import { NuevaVentaPage } from '@/pages/ventas/NuevaVentaPage';
import { productosService } from '@/api/services/productos.service';
import { ventaService } from '@/api/services/venta.service';
import axios from 'axios';

vi.mock('@/api/services/productos.service', () => ({
  productosService: {
    buscarProductos: vi.fn(),
    obtenerStock: vi.fn(),
  },
}));

vi.mock('@/api/services/venta.service', () => ({
  ventaService: {
    procesarVenta: vi.fn(),
  },
}));

const mockedProductosService = vi.mocked(productosService);
const mockedVentaService = vi.mocked(ventaService);

describe('NuevaVentaPage (HU-01)', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Mock de window.confirm para evitar bloqueos en tests
    vi.spyOn(window, 'confirm').mockReturnValue(true);
  });

  // =========================================================================
  // ESTADO 1: IDLE (carrito vacío)
  // =========================================================================
  it('muestra el estado idle con header y carrito vacío al cargar', () => {
    renderWithProviders(<NuevaVentaPage />);

    // Header visible
    expect(screen.getByText(/POS — Nueva Venta/i)).toBeInTheDocument();
    expect(screen.getByText(/Juan Pérez/i)).toBeInTheDocument();
    expect(screen.getByText(/Caja: 01/i)).toBeInTheDocument();

    // Carrito vacío
    expect(screen.getByText(/carrito vacío/i)).toBeInTheDocument();

    // Input de búsqueda visible
    expect(
      screen.getByRole('textbox', { name: /buscar producto/i }),
    ).toBeInTheDocument();

    // Botón de confirmar NO visible (carrito vacío)
    expect(screen.queryByText(/Confirmar Venta/i)).not.toBeInTheDocument();
  });

  // =========================================================================
  // FLUJO: Agregar producto al carrito
  // =========================================================================
  it('agrega un producto al carrito al buscarlo y presionar Enter', async () => {
    mockedProductosService.buscarProductos.mockResolvedValueOnce({
      productos: [
        {
          producto_id: 'P-001',
          codigo: 'CAM-001',
          nombre: 'Camiseta Básica Azul',
          precio: 25.0,
          categoria: 'Indumentaria',
          stock_actual: 5,
          estado: 'ACTIVO',
        },
      ],
      mensaje: 'Se encontraron 1 producto(s).',
    });

    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup();

    renderWithProviders(<NuevaVentaPage />);

    const input = screen.getByRole('textbox', { name: /buscar producto/i });
    await user.type(input, 'CAM-001{enter}');

    // Verifica que se agregó al carrito
    await waitFor(() => {
      expect(screen.getByText('Camiseta Básica Azul')).toBeInTheDocument();
      expect(screen.getByText(/SKU: CAM-001/i)).toBeInTheDocument();
      expect(screen.getByText(/\$25.00/)).toBeInTheDocument();
      expect(screen.getByText(/5 disponibles/i)).toBeInTheDocument();
    });

    // Resumen visible
    expect(screen.getByText(/Total de artículos/i)).toBeInTheDocument();
    expect(screen.getByText(/Total a Pagar/i)).toBeInTheDocument();
  });

  // =========================================================================
  // ESTADO: Producto no encontrado
  // =========================================================================
  it('muestra mensaje de error cuando el producto no existe', async () => {
    mockedProductosService.buscarProductos.mockResolvedValueOnce({
      productos: [],
      mensaje: 'No se encontraron productos.',
    });

    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup();

    renderWithProviders(<NuevaVentaPage />);

    const input = screen.getByRole('textbox', { name: /buscar producto/i });
    await user.type(input, 'XYZ-999{enter}');

    await waitFor(() => {
      expect(screen.getByText(/producto no encontrado/i)).toBeInTheDocument();
    });
  });

  // =========================================================================
  // FLUJO: Ajustar cantidad
  // =========================================================================
  it('permite ajustar la cantidad y actualiza el subtotal', async () => {
    mockedProductosService.buscarProductos.mockResolvedValueOnce({
      productos: [
        {
          producto_id: 'P-001',
          codigo: 'CAM-001',
          nombre: 'Camiseta',
          precio: 25.0,
          categoria: 'Indumentaria',
          stock_actual: 5,
          estado: 'ACTIVO',
        },
      ],
      mensaje: 'Se encontraron 1 producto(s).',
    });

    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup();

    renderWithProviders(<NuevaVentaPage />);

    const input = screen.getByRole('textbox', { name: /buscar producto/i });
    await user.type(input, 'CAM-001{enter}');

    await waitFor(() => {
      expect(screen.getByText('Camiseta')).toBeInTheDocument();
    });

    // Ajustar cantidad a 3 usando el botón +
    const incrementButton = screen.getByRole('button', { name: /aumentar cantidad/i });
    await user.click(incrementButton);
    await user.click(incrementButton);

    // Verifica subtotal actualizado (25 x 3 = 75)
    await waitFor(() => {
      expect(screen.getByText(/\$75.00/)).toBeInTheDocument();
    });
  });

  // =========================================================================
  // ESTADO: Stock insuficiente (alerta + botón bloqueado)
  // =========================================================================
  it('muestra alerta y bloquea botón cuando hay producto sin stock', async () => {
    mockedProductosService.buscarProductos
      .mockResolvedValueOnce({
        productos: [
          {
            producto_id: 'P-001',
            codigo: 'CAM-001',
            nombre: 'Camiseta',
            precio: 25.0,
            categoria: 'Indumentaria',
            stock_actual: 5,
            estado: 'ACTIVO',
          },
        ],
        mensaje: 'Se encontraron 1 producto(s).',
      })
      .mockResolvedValueOnce({
        productos: [
          {
            producto_id: 'P-002',
            codigo: 'PAN-042',
            nombre: 'Pantalón Deportivo',
            precio: 40.0,
            categoria: 'Indumentaria',
            stock_actual: 0,
            estado: 'ACTIVO',
          },
        ],
        mensaje: 'Se encontraron 1 producto(s).',
      });

    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup();

    renderWithProviders(<NuevaVentaPage />);

    const input = screen.getByRole('textbox', { name: /buscar producto/i });

    // Agregar producto con stock
    await user.type(input, 'CAM-001{enter}');
    await waitFor(() => expect(screen.getByText('Camiseta')).toBeInTheDocument());

    // Limpiar input y agregar producto sin stock
    await user.clear(input);
    await user.type(input, 'PAN-042{enter}');
    await waitFor(() => expect(screen.getByText('Pantalón Deportivo')).toBeInTheDocument());

    // Verifica alerta de stock
    await waitFor(() => {
      expect(
        screen.getByText(/no se puede procesar la venta/i),
      ).toBeInTheDocument();
      expect(
        screen.getByText(/pantalón deportivo.*no tiene stock/i),
      ).toBeInTheDocument();
    });

    // Verifica botón bloqueado
    const confirmButton = screen.getByRole('button', { name: /confirmar venta/i });
    expect(confirmButton).toBeDisabled();
  });

  // =========================================================================
  // FLUJO: Venta exitosa
  // =========================================================================
  it('muestra modal de éxito después de procesar la venta', async () => {
    mockedProductosService.buscarProductos.mockResolvedValueOnce({
      productos: [
        {
          producto_id: 'P-001',
          codigo: 'CAM-001',
          nombre: 'Camiseta',
          precio: 25.0,
          categoria: 'Indumentaria',
          stock_actual: 5,
          estado: 'ACTIVO',
        },
      ],
      mensaje: 'Se encontraron 1 producto(s).',
    });

    mockedVentaService.procesarVenta.mockResolvedValueOnce({
      id: 'venta-123',
      numero_ticket: 'TK-20260622-001',
      fecha_hora: '2026-06-22T14:30:00Z',
      vendedor_id: 'V-001',
      estado: 'COMPLETADA',
      items: [{ producto_id: 'P-001', cantidad: 1 }],
      descuento: { porcentaje: 0.0 },
    });

    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup();

    renderWithProviders(<NuevaVentaPage />);

    // Agregar producto
    const input = screen.getByRole('textbox', { name: /buscar producto/i });
    await user.type(input, 'CAM-001{enter}');
    await waitFor(() => expect(screen.getByText('Camiseta')).toBeInTheDocument());

    // Confirmar venta
    const confirmButton = screen.getByRole('button', { name: /confirmar venta/i });
    await user.click(confirmButton);

    // Verifica modal de éxito
    await waitFor(() => {
      expect(screen.getByText(/¡venta exitosa!/i)).toBeInTheDocument();
      expect(screen.getByText(/TK-20260622-001/i)).toBeInTheDocument();
      expect(screen.getByText(/\$25.00/)).toBeInTheDocument();
    });
  });

  // =========================================================================
  // ESTADO: Error del backend
  // =========================================================================
  it('muestra error del backend cuando la venta falla', async () => {
    mockedProductosService.buscarProductos.mockResolvedValueOnce({
      productos: [
        {
          producto_id: 'P-001',
          codigo: 'CAM-001',
          nombre: 'Camiseta',
          precio: 25.0,
          categoria: 'Indumentaria',
          stock_actual: 5,
          estado: 'ACTIVO',
        },
      ],
      mensaje: 'Se encontraron 1 producto(s).',
    });

    const axiosError = Object.assign(new Error('Request failed'), {
      isAxiosError: true,
      response: {
        status: 409,
        data: {
          error: 'STOCK_INSUFICIENTE',
          mensaje: 'Stock insuficiente al procesar la venta.',
          producto_id: 'P-001',
        },
      },
    });

    vi.spyOn(axios, 'isAxiosError').mockReturnValue(true);
    mockedVentaService.procesarVenta.mockRejectedValueOnce(axiosError);

    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup();

    renderWithProviders(<NuevaVentaPage />);

    const input = screen.getByRole('textbox', { name: /buscar producto/i });
    await user.type(input, 'CAM-001{enter}');
    await waitFor(() => expect(screen.getByText('Camiseta')).toBeInTheDocument());

    const confirmButton = screen.getByRole('button', { name: /confirmar venta/i });
    await user.click(confirmButton);

    await waitFor(() => {
      expect(
        screen.getByText(/stock insuficiente al procesar la venta/i),
      ).toBeInTheDocument();
    });
  });

  // =========================================================================
  // FLUJO: Cancelar venta
  // =========================================================================
  it('limpia el carrito al cancelar la venta', async () => {
    mockedProductosService.buscarProductos.mockResolvedValueOnce({
      productos: [
        {
          producto_id: 'P-001',
          codigo: 'CAM-001',
          nombre: 'Camiseta',
          precio: 25.0,
          categoria: 'Indumentaria',
          stock_actual: 5,
          estado: 'ACTIVO',
        },
      ],
      mensaje: 'Se encontraron 1 producto(s).',
    });

    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup();

    renderWithProviders(<NuevaVentaPage />);

    const input = screen.getByRole('textbox', { name: /buscar producto/i });
    await user.type(input, 'CAM-001{enter}');
    await waitFor(() => expect(screen.getByText('Camiseta')).toBeInTheDocument());

    // Cancelar venta
    const cancelButton = screen.getByRole('button', { name: /cancelar/i });
    await user.click(cancelButton);

    // Verifica que el carrito se limpió
    await waitFor(() => {
      expect(screen.getByText(/carrito vacío/i)).toBeInTheDocument();
    });
  });
});
