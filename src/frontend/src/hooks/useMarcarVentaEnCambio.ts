import { useMutation } from '@tanstack/react-query';
import { ventaService } from '@/api/services/venta.service';
import type { MarcarEnCambioResponse } from '@/types/api';

/**
 * Retiene un ticket marcando su venta como EN_CAMBIO (HU-04).
 *
 * El error queda como `unknown`; la página lo normaliza con
 * `normalizarErrorApi` (ej. VENTA_YA_EN_CAMBIO).
 */
export function useMarcarVentaEnCambio() {
  return useMutation<MarcarEnCambioResponse, unknown, string>({
    mutationFn: (numeroTicket) => ventaService.marcarVentaEnCambio(numeroTicket),
  });
}
