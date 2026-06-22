import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor } from '@/test/test-utils';
import { SaleTicketView } from '@/components/ventas/SaleTicketView';
import type { ItemCarrito, VentaProcesada } from '@/types/domain';

const mockCarrito: ItemCarrito[] = [
  {
    productoId: 'P-001',
    codigo: 'CAM-001',
    nombre: 'Camiseta Básica Azul',
    categoria: 'Indumentaria',
    precio: 25.0,
    stockActual: 5,
    cantidad: 2,
  },
];

const mockVentaProcesada: VentaProcesada = {
  id: 'venta-123',
  numeroTicket: 'TK-20260622-001',
  fechaHora: '2026-06-22T14:30:00Z',
  vendedorId: 'V-001',
  estado: 'COMPLETADA',
  items: [{ productoId: 'P-001', cantidad: 2 }],
  descuento: { porcentaje: 0.0 },
};

describe('SaleTicketView', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  // =========================================================================
  // ESTADO 1: IDLE (ticket visible, botón "Imprimir" disponible)
  // =========================================================================
  it('muestra el ticket y el botón "Imprimir Ticket" en estado idle', () => {
    const onNuevaVenta = vi.fn();

    renderWithProviders(
      <SaleTicketView
        carrito={mockCarrito}
        ventaProcesada={mockVentaProcesada}
        totalArticulos={2}
        totalPagar={50.0}
        onNuevaVenta={onNuevaVenta}
      />,
    );

    // Ticket visible
    expect(screen.getByText('TK-20260622-001')).toBeInTheDocument();
    expect(screen.getByText('Camiseta Básica Azul')).toBeInTheDocument();

    // Botón de imprimir visible
    expect(
      screen.getByRole('button', { name: /imprimir ticket/i }),
    ).toBeInTheDocument();

    // Indicador de impresora en estado idle
    expect(screen.getByText(/impresora lista/i)).toBeInTheDocument();
  });

  // =========================================================================
  // FLUJO: Imprimir → printing → success → Nueva Venta
  // =========================================================================
  it('simula la impresión y muestra botón "Nueva Venta" al finalizar', async () => {
    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
    const onNuevaVenta = vi.fn();

    renderWithProviders(
      <SaleTicketView
        carrito={mockCarrito}
        ventaProcesada={mockVentaProcesada}
        totalArticulos={2}
        totalPagar={50.0}
        onNuevaVenta={onNuevaVenta}
      />,
    );

    // Click en "Imprimir Ticket"
    const printButton = screen.getByRole('button', { name: /imprimir ticket/i });
    await user.click(printButton);

    // Estado: printing
    await waitFor(() => {
      expect(screen.getByText(/imprimiendo ticket/i)).toBeInTheDocument();
    });
    expect(screen.getByText(/imprimiendo/i)).toBeInTheDocument();

    // Avanza el tiempo para completar la impresión
    act(() => {
      vi.advanceTimersByTime(1500);
    });

    // Estado: success → aparece botón "Nueva Venta"
    await waitFor(() => {
      expect(screen.getByText(/impresión exitosa/i)).toBeInTheDocument();
    });
    expect(
      screen.getByRole('button', { name: /nueva venta/i }),
    ).toBeInTheDocument();
  });

  // =========================================================================
  // FLUJO: Omitir impresión → limpia todo
  // =========================================================================
  it('llama a onNuevaVenta al presionar "Omitir Impresión"', async () => {
    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup();
    const onNuevaVenta = vi.fn();

    renderWithProviders(
      <SaleTicketView
        carrito={mockCarrito}
        ventaProcesada={mockVentaProcesada}
        totalArticulos={2}
        totalPagar={50.0}
        onNuevaVenta={onNuevaVenta}
      />,
    );

    const skipButton = screen.getByRole('button', { name: /omitir impresión/i });
    await user.click(skipButton);

    expect(onNuevaVenta).toHaveBeenCalledTimes(1);
  });

  // =========================================================================
  // FLUJO: Nueva Venta después de impresión exitosa
  // =========================================================================
  it('llama a onNuevaVenta al presionar "Nueva Venta" después de imprimir', async () => {
    const { userEvent } = await import('@/test/test-utils');
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
    const onNuevaVenta = vi.fn();

    renderWithProviders(
      <SaleTicketView
        carrito={mockCarrito}
        ventaProcesada={mockVentaProcesada}
        totalArticulos={2}
        totalPagar={50.0}
        onNuevaVenta={onNuevaVenta}
      />,
    );

    // Imprimir
    await user.click(screen.getByRole('button', { name: /imprimir ticket/i }));
    act(() => {
      vi.advanceTimersByTime(1500);
    });

    // Nueva Venta
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /nueva venta/i })).toBeInTheDocument();
    });
    await user.click(screen.getByRole('button', { name: /nueva venta/i }));

    expect(onNuevaVenta).toHaveBeenCalledTimes(1);
  });

  // =========================================================================
  // RENDER: Información del ticket
  // =========================================================================
  it('muestra el resumen de la venta procesada', () => {
    const onNuevaVenta = vi.fn();

    renderWithProviders(
      <SaleTicketView
        carrito={mockCarrito}
        ventaProcesada={mockVentaProcesada}
        totalArticulos={2}
        totalPagar={50.0}
        onNuevaVenta={onNuevaVenta}
      />,
    );

    expect(screen.getByText(/venta procesada correctamente/i)).toBeInTheDocument();
    expect(screen.getByText(/TK-20260622-001/i)).toBeInTheDocument();
  });
});
