import { useMemo } from 'react';
import type { ItemCarrito, ValidacionCarrito, ErrorValidacionItem } from '@/types/domain';

interface UseCartValidationResult {
  /** Resultado de la validación */
  validacion: ValidacionCarrito;
  /** Si el carrito es procesable (sin errores) */
  esProcesable: boolean;
}

/**
 * Hook que valida el carrito localmente antes de enviarlo al backend.
 *
 * 🎯 Reglas de negocio validadas (SRP):
 * - Stock > 0 para cada producto
 * - Cantidad <= stock_actual para cada producto
 * - Cantidad > 0 para cada producto
 *
 * ⚠️ Esta validación es LOCAL (UI). El backend también valida (HU-01).
 *    El objetivo es dar feedback inmediato al vendedor.
 */
export function useCartValidation(items: ItemCarrito[]): UseCartValidationResult {
  const validacion = useMemo<ValidacionCarrito>(() => {
    const errores: ErrorValidacionItem[] = [];

    for (const item of items) {
      if (item.cantidad <= 0) {
        errores.push({
          productoId: item.productoId,
          nombre: item.nombre,
          motivo: 'CANTIDAD_CERO',
          mensaje: `El producto "${item.nombre}" tiene cantidad 0.`,
        });
      } else if (item.stockActual === 0) {
        errores.push({
          productoId: item.productoId,
          nombre: item.nombre,
          motivo: 'SIN_STOCK',
          mensaje: `El producto "${item.nombre}" no tiene stock disponible.`,
        });
      } else if (item.cantidad > item.stockActual) {
        errores.push({
          productoId: item.productoId,
          nombre: item.nombre,
          motivo: 'CANTIDAD_EXCEDE_STOCK',
          mensaje: `El producto "${item.nombre}" solo tiene ${item.stockActual} unidades disponibles.`,
        });
      }
    }

    return {
      esValido: errores.length === 0,
      errores,
    };
  }, [items]);

  const esProcesable = validacion.esValido && items.length > 0;

  return {
    validacion,
    esProcesable,
  };
}
