import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ReceiptTicket } from '@/components/ui';
import type { Ticket } from '@/types/domain';

const mockTicket: Ticket = {
  numeroTicket: 'TK-20260622-001',
  fechaHora: '2026-06-22T14:30:00Z',
  vendedorId: 'V-001',
  estado: 'COMPLETADA',
  totalArticulos: 3,
  totalPagar: 90.0,
  items: [
    {
      productoId: 'P-001',
      nombre: 'Camiseta Básica Azul',
      cantidad: 2,
      precioUnitario: 25.0,
      subtotal: 50.0,
    },
    {
      productoId: 'P-002',
      nombre: 'Pantalón Deportivo',
      cantidad: 1,
      precioUnitario: 40.0,
      subtotal: 40.0,
    },
  ],
};

describe('ReceiptTicket', () => {
  it('renderiza el número de ticket', () => {
    render(<ReceiptTicket ticket={mockTicket} />);

    expect(screen.getByText('TK-20260622-001')).toBeInTheDocument();
  });

  it('renderiza el nombre del negocio por defecto', () => {
    render(<ReceiptTicket ticket={mockTicket} />);

    expect(screen.getByText(/SGVIR Retail/i)).toBeInTheDocument();
  });

  it('renderiza un nombre de negocio personalizado', () => {
    render(<ReceiptTicket ticket={mockTicket} nombreNegocio="Mi Tienda" />);

    expect(screen.getByText('Mi Tienda')).toBeInTheDocument();
    expect(screen.queryByText(/SGVIR Retail/i)).not.toBeInTheDocument();
  });

  it('renderiza el ID del vendedor', () => {
    render(<ReceiptTicket ticket={mockTicket} />);

    expect(screen.getByText('V-001')).toBeInTheDocument();
  });

  it('renderiza el estado de la venta', () => {
    render(<ReceiptTicket ticket={mockTicket} />);

    expect(screen.getByText('COMPLETADA')).toBeInTheDocument();
  });

  it('renderiza todos los items del ticket', () => {
    render(<ReceiptTicket ticket={mockTicket} />);

    expect(screen.getByText('Camiseta Básica Azul')).toBeInTheDocument();
    expect(screen.getByText('Pantalón Deportivo')).toBeInTheDocument();
  });

  it('renderiza las cantidades de cada item', () => {
    render(<ReceiptTicket ticket={mockTicket} />);

    // Cantidad de Camiseta: 2
    // Cantidad de Pantalón: 1
    expect(screen.getByText('2')).toBeInTheDocument();
    expect(screen.getByText('1')).toBeInTheDocument();
  });

  it('renderiza los subtotales de cada item', () => {
    render(<ReceiptTicket ticket={mockTicket} />);

    // $50.00 (Camiseta) y $40.00 (Pantalón)
    expect(screen.getByText('$50,00')).toBeInTheDocument();
    expect(screen.getByText('$40,00')).toBeInTheDocument();
  });

  it('renderiza el total a pagar', () => {
    render(<ReceiptTicket ticket={mockTicket} />);

    expect(screen.getByText('$90,00')).toBeInTheDocument();
  });

  it('renderiza el total de artículos', () => {
    render(<ReceiptTicket ticket={mockTicket} />);

    expect(screen.getByText('3')).toBeInTheDocument();
  });

  it('renderiza el mensaje de agradecimiento', () => {
    render(<ReceiptTicket ticket={mockTicket} />);

    expect(screen.getByText(/¡Gracias por su compra!/i)).toBeInTheDocument();
    expect(
      screen.getByText(/Conserve este ticket para cambios/i),
    ).toBeInTheDocument();
  });

  it('renderiza el código de barras simulado con el número de ticket', () => {
    render(<ReceiptTicket ticket={mockTicket} />);

    // El código de barras muestra el número de ticket debajo
    const barcodeNumber = screen.getByText('TK-20260622-001');
    expect(barcodeNumber).toBeInTheDocument();
  });

  it('formatea la fecha correctamente', () => {
    render(<ReceiptTicket ticket={mockTicket} />);

    // La fecha debe estar formateada en es-AR
    // 22/06/2026, 14:30 (o similar según el locale)
    const fechaElement = screen.getByText(/22\/06\/2026/);
    expect(fechaElement).toBeInTheDocument();
  });

  it('tiene aria-label para accesibilidad', () => {
    render(<ReceiptTicket ticket={mockTicket} />);

    const article = screen.getByRole('article', { name: /ticket de venta/i });
    expect(article).toBeInTheDocument();
  });
});
