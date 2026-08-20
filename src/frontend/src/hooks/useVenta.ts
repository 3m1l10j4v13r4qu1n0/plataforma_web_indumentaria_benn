import { useMutation } from '@tanstack/react-query';
import { ventaService } from '@/api/services/venta.service';
import type { CrearVentaRequest, VentaResponse } from '@/types/api';

/**
 * Procesa una venta: valida stock y descuenta inventario en el backend (HU-01).
 *
 * El error queda como `unknown`; la página lo normaliza con `normalizarErrorApi`
 * para obtener un mensaje amigable (ej. STOCK_INSUFICIENTE).
 */
export function useVenta() {
  return useMutation<VentaResponse, unknown, CrearVentaRequest>({
    mutationFn: (request) => ventaService.procesarVenta(request),
  });
}