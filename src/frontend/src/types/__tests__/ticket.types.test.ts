import { describe, it, expect } from 'vitest';
import { toTicket } from '@/types/api';
import type { ItemCarrito } from '@/types/domain';

describe('toTicket (mapper local → Ticket)', () => {
  it('construye un Ticket completo desde datos locales del carrito', () => {
    const carrito: ItemCarrito[] = [
      {
        productoId: 'P-001',
        codigo: 'CAM-001',
        nombre: 'Camiseta Básica Azul',
        categoria: 'Indumentaria',
        precio: 25.0,
        stockActual: 5,
        cantidad: 2,
      },
      {
        productoId: 'P-002',
        codigo: 'PAN-042',
        nombre: 'Pantalón Deportivo',
        categoria: 'Indumentaria',
        precio: 40.0,
        stockActual: 3,
        cantidad: 1,
      },
    ];

    const result = toTicket({
      carrito,
      numeroTicket: 'TK-20260622-001',
      fechaHora: '2026-06-22T14:30:00Z',
      vendedorId: 'V-001',
      estado: 'COMPLETADA',
      totalArticulos: 3,
      totalPagar: 90.0,
    });

    expect(result).toEqual({
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
          subtotal: 50.0, // 25 × 2
        },
        {
          productoId: 'P-002',
          nombre: 'Pantalón Deportivo',
          cantidad: 1,
          precioUnitario: 40.0,
          subtotal: 40.0, // 40 × 1
        },
      ],
    });
  });

  it('calcula correctamente el subtotal (precio × cantidad)', () => {
    const carrito: ItemCarrito[] = [
      {
        productoId: 'P-001',
        codigo: 'CAM-001',
        nombre: 'Producto',
        categoria: 'Test',
        precio: 33.33,
        stockActual: 10,
        cantidad: 3,
      },
    ];

    const result = toTicket({
      carrito,
      numeroTicket: 'TK-001',
      fechaHora: '2026-06-22T14:30:00Z',
      vendedorId: 'V-001',
      estado: 'COMPLETADA',
      totalArticulos: 3,
      totalPagar: 99.99,
    });

    // 33.33 × 3 = 99.99
    expect(result.items[0].subtotal).toBeCloseTo(99.99, 2);
  });

  it('maneja un carrito vacío (caso borde)', () => {
    const result = toTicket({
      carrito: [],
      numeroTicket: 'TK-001',
      fechaHora: '2026-06-22T14:30:00Z',
      vendedorId: 'V-001',
      estado: 'COMPLETADA',
      totalArticulos: 0,
      totalPagar: 0,
    });

    expect(result.items).toEqual([]);
    expect(result.totalArticulos).toBe(0);
    expect(result.totalPagar).toBe(0);
  });
});
