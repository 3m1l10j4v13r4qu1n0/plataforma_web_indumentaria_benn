import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi, beforeEach } from 'vitest';
import { ConsultarStockPage } from './ConsultarStockPage';
import { productosService } from '@/api/services/productos.service';

vi.mock('@/api/services/productos.service', () => ({
  productosService: {
    buscarStock: vi.fn(),
  },
}));

describe('ConsultarStockPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('muestra resultados cuando el usuario busca por nombre o código', async () => {
    vi.mocked(productosService.buscarStock).mockResolvedValue({
      productos: [
        {
          producto_id: 'prod-1',
          nombre: 'Camiseta Básica',
          stock_actual: 5,
        },
      ],
      mensaje: 'Se encontraron 1 producto(s) coincidente(s).',
    });

    const user = userEvent.setup();
    render(<ConsultarStockPage />);

    const input = screen.getByRole('textbox', { name: /buscar producto/i });
    await user.type(input, 'cam');
    await user.keyboard('{Enter}');

    expect(await screen.findByText('Camiseta Básica')).toBeInTheDocument();
    expect(screen.getByText(/5/i)).toBeInTheDocument();
  });
});
