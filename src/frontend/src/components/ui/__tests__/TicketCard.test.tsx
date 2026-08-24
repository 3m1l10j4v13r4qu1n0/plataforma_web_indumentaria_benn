import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TicketCard } from '@/components/ui';
import type { VentaResponse } from '@/types/api';

const venta: VentaResponse = {
  id: 'V-100',
  fecha_hora: '2026-06-05T14:45:30',
  vendedor_id: 'V-001',
  estado: 'CONFIRMADA',
  numero_ticket: 'T-20260605-142',
  total: 110,
  mensaje: 'Venta registrada y ticket generado exitosamente.',
  items: [
    { producto_id: 'CAM-001', nombre: 'Camiseta Básica Azul', cantidad: 1, precio: 25 },
    { producto_id: 'ZAP-042', nombre: 'Zapatillas Running T-42', cantidad: 1, precio: 85 },
  ],
};

function renderizar(props: { advertenciaImpresion?: boolean } = {}) {
  return render(
    <TicketCard
      venta={venta}
      onImprimir={vi.fn()}
      onCerrar={vi.fn()}
      {...props}
    />,
  );
}

describe('TicketCard (HU-07)', () => {
  it('muestra el header de éxito y el branding del contrato', () => {
    renderizar();

    expect(screen.getByText('¡Venta Registrada!')).toBeInTheDocument();
    expect(screen.getByText('TIENDA RETAIL S.A.')).toBeInTheDocument();
    expect(screen.getByText('RUC: 20123456789')).toBeInTheDocument();
    expect(screen.getByText('05 Jun 2026 - 14:45:30')).toBeInTheDocument();
  });

  it('muestra los ítems en formato comprobante y el total', () => {
    renderizar();

    expect(screen.getByText('1x Camiseta Básica Azul')).toBeInTheDocument();
    expect(screen.getByText('1x Zapatillas Running T-42')).toBeInTheDocument();
    expect(screen.getByText('$25.00')).toBeInTheDocument();
    expect(screen.getByText('$85.00')).toBeInTheDocument();
    expect(screen.getByText('$110.00')).toBeInTheDocument();
  });

  it('etiqueta el número como COMPROBANTE N°', () => {
    renderizar();

    expect(screen.getByText('COMPROBANTE N°')).toBeInTheDocument();
    expect(screen.getByText('T-20260605-142')).toBeInTheDocument();
  });

  it('muestra las acciones contractuales e invoca los callbacks', async () => {
    const user = userEvent.setup();
    const onImprimir = vi.fn();
    const onCerrar = vi.fn();
    render(
      <TicketCard
        venta={venta}
        onImprimir={onImprimir}
        onCerrar={onCerrar}
      />,
    );

    await user.click(screen.getByRole('button', { name: 'Imprimir Comprobante' }));
    await user.click(screen.getByRole('button', { name: 'Nueva venta' }));

    expect(onImprimir).toHaveBeenCalledTimes(1);
    expect(onCerrar).toHaveBeenCalledTimes(1);
  });

  it('muestra el toast de impresora desconectada sin anular la venta (E-07)', async () => {
    const user = userEvent.setup();
    const onImprimir = vi.fn();
    render(
      <TicketCard
        venta={venta}
        onImprimir={onImprimir}
        onCerrar={vi.fn()}
        advertenciaImpresion
      />,
    );

    expect(screen.getByRole('alert')).toBeInTheDocument();
    expect(
      screen.getByText(
        'La venta se registró, pero la impresora está desconectada. ¿Desea reintentar?',
      ),
    ).toBeInTheDocument();

    // La venta sigue visible y exitosa; reintentar vuelve a llamar a imprimir
    expect(screen.getByText('¡Venta Registrada!')).toBeInTheDocument();
    await user.click(screen.getByText('Reintentar impresión'));
    expect(onImprimir).toHaveBeenCalledTimes(1);
  });
});
