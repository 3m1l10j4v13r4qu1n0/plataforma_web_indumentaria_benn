import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { VentaItemRow, type VentaItem } from '@/components/ui';

const item: VentaItem = {
  productoId: 'P-001',
  nombre: 'Remera Azul',
  precio: 15000,
  cantidad: 2,
};

describe('VentaItemRow', () => {
  it('muestra nombre, cantidad × precio y subtotal', () => {
    render(<VentaItemRow item={item} onQuitar={vi.fn()} />);

    expect(screen.getByText('Remera Azul')).toBeInTheDocument();
    expect(screen.getByText('2 × $15000')).toBeInTheDocument();
    expect(screen.getByText('$30000')).toBeInTheDocument();
  });

  it('llama onQuitar al hacer clic en Quitar', async () => {
    const user = userEvent.setup();
    const onQuitar = vi.fn();

    render(<VentaItemRow item={item} onQuitar={onQuitar} />);

    await user.click(screen.getByRole('button', { name: 'Quitar Remera Azul de la venta' }));
    expect(onQuitar).toHaveBeenCalledTimes(1);
  });
});