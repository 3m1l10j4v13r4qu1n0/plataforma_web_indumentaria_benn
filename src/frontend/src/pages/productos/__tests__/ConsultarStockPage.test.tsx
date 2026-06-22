import { describe, it, expect, vi, beforeEach } from 'vitest';
import { screen, waitFor } from '@/test/test-utils';
import { ConsultarStockPage } from '@/pages/productos/ConsultarStockPage';
import { productosService } from '@/api/services/productos.service';

vi.mock('@/api/services/productos.service', () => ({
  productosService: {
    buscarProductos: vi.fn(),
  },
}));

const mockedService = vi.mocked(productosService);

describe('ConsultarStockPage (HU-06)', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // =========================================================================
  // ESTADO 1: IDLE (sin búsqueda aún)
  // =========================================================================
  it('muestra el estado idle al cargar inicialmente', () => {
    renderWithProviders(<ConsultarStockPage />);

    expect(
      screen.getByRole('heading', { name: /comienza tu búsqueda/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/escribe el nombre o código de un producto/i),
    ).toBeInTheDocument();

    // El servicio NO debe haber sido llamado
    expect(mockedService.buscarProductos).not.toHaveBeenCalled();
  });

  // =========================================================================
  // ESTADO 2: LOADING (búsqueda en progreso)
  // =========================================================================
  it('muestra el estado loading mientras busca', async () => {
    // El servicio nunca resuelve (simula carga infinita)
    mockedService.buscarProductos.mockImplementation(
      () => new Promise(() => {}),
    );

    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup();

    renderWithProviders(<ConsultarStockPage />);

    const input = screen.getByRole('textbox', {
      name: /buscar producto por nombre o código/i,
    });

    await user.type(input, 'camiseta{enter}');

    await waitFor(() => {
      expect(
        screen.getByText(/buscando productos para "camiseta"/i),
      ).toBeInTheDocument();
    });
  });

  // =========================================================================
  // ESTADO 3: ERROR (fallo en la petición)
  // =========================================================================
  it('muestra el estado error cuando el servicio falla', async () => {
    mockedService.buscarProductos.mockRejectedValueOnce(
      new Error('Network Error'),
    );

    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup();

    renderWithProviders(<ConsultarStockPage />);

    const input = screen.getByRole('textbox', {
      name: /buscar producto por nombre o código/i,
    });

    await user.type(input, 'camiseta{enter}');

    await waitFor(() => {
      expect(
        screen.getByRole('alert', { name: /error al consultar stock/i }),
      ).toBeInTheDocument();
    });

    expect(screen.getByText(/network error/i)).toBeInTheDocument();
  });

  // =========================================================================
  // ESTADO 4: EMPTY (búsqueda exitosa pero sin resultados)
  // =========================================================================
  it('muestra el estado empty cuando no hay resultados', async () => {
    mockedService.buscarProductos.mockResolvedValueOnce({
      productos: [],
      total: 0,
    });

    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup();

    renderWithProviders(<ConsultarStockPage />);

    const input = screen.getByRole('textbox', {
      name: /buscar producto por nombre o código/i,
    });

    await user.type(input, 'producto-inexistente{enter}');

    await waitFor(() => {
      expect(
        screen.getByText(/no se encontraron productos que coincidan con/i),
      ).toBeInTheDocument();
    });

    expect(
      screen.getByText(/"producto-inexistente"/i),
    ).toBeInTheDocument();
  });

  // =========================================================================
  // ESTADO 5: SUCCESS (lista de productos)
  // =========================================================================
  it('muestra la lista de productos cuando la búsqueda es exitosa', async () => {
    mockedService.buscarProductos.mockResolvedValueOnce({
      productos: [
        {
          codigo: 'CAM-001',
          nombre: 'Camiseta Básica Azul',
          categoria: 'Indumentaria',
          stock_actual: 24,
          stock_minimo: 5,
          actualizado_en: '2026-06-22T14:33:00Z',
        },
        {
          codigo: 'CAM-002',
          nombre: 'Camiseta Básica Roja',
          categoria: 'Indumentaria',
          stock_actual: 2,
          stock_minimo: 5,
          actualizado_en: '2026-06-22T14:30:00Z',
        },
      ],
      total: 2,
    });

    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup();

    renderWithProviders(<ConsultarStockPage />);

    const input = screen.getByRole('textbox', {
      name: /buscar producto por nombre o código/i,
    });

    await user.type(input, 'camiseta{enter}');

    // Verifica que se muestran los productos
    await waitFor(() => {
      expect(screen.getByText('Camiseta Básica Azul')).toBeInTheDocument();
      expect(screen.getByText('Camiseta Básica Roja')).toBeInTheDocument();
    });

    // Verifica el contador de resultados
    expect(screen.getByText(/resultados encontrados/i)).toBeInTheDocument();
    expect(screen.getByText('(2)')).toBeInTheDocument();

    // Verifica los códigos
    expect(screen.getByText('CAM-001')).toBeInTheDocument();
    expect(screen.getByText('CAM-002')).toBeInTheDocument();

    // Verifica los badges de stock (24 saludable, 2 bajo)
    expect(screen.getByText(/24 en stock/i)).toBeInTheDocument();
    expect(screen.getByText(/2 stock bajo/i)).toBeInTheDocument();
  });

  // =========================================================================
  // COMPORTAMIENTO: No dispara búsqueda sin Enter
  // =========================================================================
  it('NO dispara la búsqueda al escribir, solo al presionar Enter', async () => {
    mockedService.buscarProductos.mockResolvedValue({ productos: [], total: 0 });

    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup();

    renderWithProviders(<ConsultarStockPage />);

    const input = screen.getByRole('textbox', {
      name: /buscar producto por nombre o código/i,
    });

    // Escribe sin Enter
    await user.type(input, 'cami');

    // El servicio NO debe haber sido llamado
    expect(mockedService.buscarProductos).not.toHaveBeenCalled();

    // Ahora presiona Enter
    await user.keyboard('{enter}');

    await waitFor(() => {
      expect(mockedService.buscarProductos).toHaveBeenCalledWith({
        query: 'cami',
      });
    });
  });
});