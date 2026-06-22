import { describe, it, expect } from 'vitest';
import { toItemCarrito, toVentaRequest, toVentaProcesada } from '@/types/api';
import type { ProductoBusquedaItem, VentaResponse } from '@/types/api';
import type { ItemCarrito } from '@/types/domain';

describe('toItemCarrito (mapper API → Domain)', () => {
  it('mapea correctamente un ProductoBusquedaItem a ItemCarrito', () => {
    const producto: ProductoBusquedaItem = {
      producto_id: 'P-001',
      codigo: 'CAM-001',
      nombre: 'Camiseta Básica Azul',
      precio: 25.0,
      categoria: 'Indumentaria',
      stock_actual: 5,
      estado: 'ACTIVO',
    };

    const result = toItemCarrito(producto);

    expect(result).toEqual({
      productoId: 'P-001',
      codigo: 'CAM-001',
      nombre: 'Camiseta Básica Azul',
      categoria: 'Indumentaria',
      precio: 25.0,
      stockActual: 5,
      cantidad: 1, // default
    });
  });

  it('permite especificar una cantidad inicial', () => {
    const producto: ProductoBusquedaItem = {
      producto_id: 'P-001',
      codigo: 'CAM-001',
      nombre: 'Camiseta',
      precio: 25.0,
      categoria: 'Indumentaria',
      stock_actual: 10,
      estado: 'ACTIVO',
    };

    const result = toItemCarrito(producto, 3);

    expect(result.cantidad).toBe(3);
  });
});

describe('toVentaRequest (mapper Domain → API)', () => {
  it('mapea el carrito al formato del backend (snake_case)', () => {
    const carrito: ItemCarrito[] = [
      {
        productoId: 'P-001',
        codigo: 'CAM-001',
        nombre: 'Camiseta',
        categoria: 'Indumentaria',
        precio: 25.0,
        stockActual: 5,
        cantidad: 2,
      },
      {
        productoId: 'P-002',
        codigo: 'PAN-042',
        nombre: 'Pantalón',
        categoria: 'Indumentaria',
        precio: 40.0,
        stockActual: 3,
        cantidad: 1,
      },
    ];

    const result = toVentaRequest(carrito, 'V-001');

    expect(result).toEqual({
      vendedor_id: 'V-001',
      items: [
        { producto_id: 'P-001', cantidad: 2 },
        { producto_id: 'P-002', cantidad: 1 },
      ],
      porcentaje_descuento: 0.0,
      gerente_autorizacion_id: undefined,
    });
  });
});

describe('toVentaProcesada (mapper API → Domain)', () => {
  it('mapea la respuesta del backend al dominio', () => {
    const response: VentaResponse = {
      id: 'venta-123',
      numero_ticket: 'TK-20260622-001',
      fecha_hora: '2026-06-22T14:30:00Z',
      vendedor_id: 'V-001',
      estado: 'COMPLETADA',
      items: [
        { producto_id: 'P-001', cantidad: 2 },
      ],
      descuento: {
        porcentaje: 0.0,
        gerente_autorizacion_id: undefined,
      },
    };

    const result = toVentaProcesada(response);

    expect(result).toEqual({
      id: 'venta-123',
      numeroTicket: 'TK-20260622-001',
      fechaHora: '2026-06-22T14:30:00Z',
      vendedorId: 'V-001',
      estado: 'COMPLETADA',
      items: [{ productoId: 'P-001', cantidad: 2 }],
      descuento: { porcentaje: 0.0, gerenteAutorizacionId: undefined },
    });
  });
});
