import { useMutation } from '@tanstack/react-query';
import { descuentoService } from '@/api/services/descuento.service';
import type { AplicarDescuentoRequest, DescuentoResponse } from '@/types/api';

/**
 * Aplica un descuento a una venta existente (HU-05).
 *
 * El error queda como `unknown`; la página lo normaliza con `normalizarErrorApi`
 * para obtener un mensaje amigable (ej. DESCUENTO_EXCEDE_LIMITE).
 */
export function useDescuento() {
  return useMutation<DescuentoResponse, unknown, AplicarDescuentoRequest>({
    mutationFn: (request) => descuentoService.aplicarDescuento(request),
  });
}
