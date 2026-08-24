import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ConsultarStockPage } from '@/pages/productos/ConsultarStockPage';

vi.mock('@/api/services/productos.service', () => ({
  productosService: {
    obtenerStock: vi.fn(),
    buscarProductos: vi.fn(),
  },
}));

import { productosService } from '@/api/services/productos.service';

const mockBuscarProductos = vi.mocked(productosService.buscarProductos);

function renderizar() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <ConsultarStockPage />
    </QueryClientProvider>,
  );
}

async function buscar(term: string) {
  const user = userEvent.setup();
  await user.type(
    screen.getByLabelText('Buscar producto por nombre o código'),
    term,
  );
  await user.keyboard('{Enter}');
}

describe('ConsultarStockPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('muestra el título del contrato y la ayuda de búsqueda', () => {
    renderizar();

    expect(
      screen.getByRole('heading', {
        name: 'Consulta de Stock en Tiempo Real',
      }),
    ).toBeInTheDocument();
    expect(screen.getByText('Enter para buscar')).toBeInTheDocument();
  });

  it('muestra los resultados con badges de stock por nivel (contrato HU-06)', async () => {
    mockBuscarProductos.mockResolvedValue({
      resultados: [
        {
          productoId: 'CAM-001',
          codigo: 'CAM-001',
          nombre: 'Camiseta Básica Azul',
          stockActual: 24,
          estado: 'ACTIVO',
        },
        {
          productoId: 'CAM-002',
          codigo: 'CAM-002',
          nombre: 'Camiseta Básica Roja',
          stockActual: 2,
          estado: 'ACTIVO',
        },
      ],
      totalEncontrados: 2,
      mensaje: null,
    });
    renderizar();

    await buscar('Camiseta');

    expect(await screen.findByText('Resultados encontrados')).toBeInTheDocument();
    expect(screen.getByText('Camiseta Básica Azul')).toBeInTheDocument();
    expect(screen.getByText('Camiseta Básica Roja')).toBeInTheDocument();
    expect(
      screen.getByLabelText('Stock: 24 unidades - 24 en stock'),
    ).toBeInTheDocument();
    expect(
      screen.getByLabelText('Stock: 2 unidades - 2 en stock'),
    ).toBeInTheDocument();
  });

  it('muestra el estado vacío contractual cuando no hay resultados (E-06)', async () => {
    mockBuscarProductos.mockResolvedValue({
      resultados: [],
      totalEncontrados: 0,
      mensaje: null,
    });
    renderizar();

    await buscar('XYZ-999');

    expect(await screen.findByText('Producto no encontrado')).toBeInTheDocument();
    expect(
      screen.getByText(
        'No existe ningún producto activo con el código o nombre "XYZ-999". Verifique el código de barras o intente con otra palabra clave.',
      ),
    ).toBeInTheDocument();
  });

  it('prioriza el mensaje del backend en el estado vacío cuando existe', async () => {
    mockBuscarProductos.mockResolvedValue({
      resultados: [],
      totalEncontrados: 0,
      mensaje: 'No hay productos activos que coincidan con la búsqueda.',
    });
    renderizar();

    await buscar('XYZ-999');

    expect(
      await screen.findByText(
        'No hay productos activos que coincidan con la búsqueda.',
      ),
    ).toBeInTheDocument();
  });
});
