import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { VentaProductoCard } from '@/components/ui';
import type { StockProducto } from '@/types/domain';

const producto: StockProducto = {
  productoId: 'P-001',
  categoria: 'Remeras',
  nombre: 'Remera Azul',
  precio: 15000,
  stockActual: 10,
};

describe('VentaProductoCard', () => {
  it('muestra nombre, precio y stock disponible', () => {
    render(
      <VentaProductoCard
        producto={producto}
        cantidad={1}
        onCantidadChange={vi.fn()}
        onAgregar={vi.fn()}
      />,
    );

    expect(screen.getByText('Remera Azul')).toBeInTheDocument();
    expect(screen.getByText('$15000.00')).toBeInTheDocument();
    expect(
      screen.getByLabelText('Stock: 10 unidades - 10 disponibles'),
    ).toBeInTheDocument();
  });

  it('deshabilita el botón y el input cuando no hay stock', () => {
    render(
      <VentaProductoCard
        producto={{ ...producto, stockActual: 0 }}
        cantidad={0}
        onCantidadChange={vi.fn()}
        onAgregar={vi.fn()}
      />,
    );

    const boton = screen.getByRole('button', { name: 'Sin stock' });
    expect(boton).toBeDisabled();
    expect(screen.getByLabelText('Cantidad a vender')).toBeDisabled();
  });

  it('llama onAgregar al hacer clic en "Agregar a venta"', async () => {
    const user = userEvent.setup();
    const onAgregar = vi.fn();

    render(
      <VentaProductoCard
        producto={producto}
        cantidad={2}
        onCantidadChange={vi.fn()}
        onAgregar={onAgregar}
      />,
    );

    await user.click(screen.getByRole('button', { name: 'Agregar a venta' }));
    expect(onAgregar).toHaveBeenCalledTimes(1);
  });

  it('muestra "Agregado" y deshabilita el botón si ya fue agregado', () => {
    render(
      <VentaProductoCard
        producto={producto}
        cantidad={1}
        onCantidadChange={vi.fn()}
        onAgregar={vi.fn()}
        yaAgregado
      />,
    );

    expect(screen.getByRole('button', { name: 'Agregado' })).toBeDisabled();
  });
});