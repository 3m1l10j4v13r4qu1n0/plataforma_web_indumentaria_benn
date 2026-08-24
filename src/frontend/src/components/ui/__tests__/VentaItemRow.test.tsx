import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { VentaItemRow, type VentaItem } from '@/components/ui';

const item: VentaItem = {
  productoId: 'P-001',
  nombre: 'Remera Azul',
  precio: 15000,
  cantidad: 2,
  stockActual: 10,
};

const itemSinStock: VentaItem = {
  ...item,
  stockActual: 0,
};

function renderizarFila(itemProps: VentaItem, handlers?: { onCantidadChange?: (n: number) => void; onQuitar?: () => void }) {
  return render(
    <table>
      <tbody>
        <VentaItemRow
          item={itemProps}
          onCantidadChange={handlers?.onCantidadChange ?? vi.fn()}
          onQuitar={handlers?.onQuitar ?? vi.fn()}
        />
      </tbody>
    </table>,
  );
}

describe('VentaItemRow', () => {
  it('muestra producto, SKU, precio unitario, badge de stock y subtotal', () => {
    renderizarFila(item);

    expect(screen.getByText('Remera Azul')).toBeInTheDocument();
    expect(screen.getByText('SKU: P-001')).toBeInTheDocument();
    expect(screen.getByText('$15000.00')).toBeInTheDocument();
    expect(
      screen.getByLabelText('Stock: 10 unidades - 10 disponibles'),
    ).toBeInTheDocument();
    expect(screen.getByText('$30000.00')).toBeInTheDocument();
  });

  it('permite editar la cantidad inline', () => {
    const onCantidadChange = vi.fn();
    renderizarFila(item, { onCantidadChange });

    const input = screen.getByLabelText('Cantidad de Remera Azul');
    fireEvent.change(input, { target: { value: '3' } });

    expect(onCantidadChange).toHaveBeenCalledWith(3);
  });

  it('resalta la fila en rojo y bloquea el input cuando no hay stock (E-01)', () => {
    renderizarFila(itemSinStock);

    const input = screen.getByLabelText('Cantidad de Remera Azul');
    expect(input).toBeDisabled();
    expect(input).toHaveValue(0);
    expect(
      screen.getByLabelText('Stock: 0 unidades - 0 disponibles'),
    ).toBeInTheDocument();
    expect(screen.getByText('SKU: P-001').closest('tr')).toHaveClass('bg-red-50');
  });

  it('llama onQuitar al hacer clic en Quitar', async () => {
    const user = userEvent.setup();
    const onQuitar = vi.fn();
    renderizarFila(item, { onQuitar });

    await user.click(
      screen.getByRole('button', { name: 'Quitar Remera Azul de la venta' }),
    );
    expect(onQuitar).toHaveBeenCalledTimes(1);
  });
});
