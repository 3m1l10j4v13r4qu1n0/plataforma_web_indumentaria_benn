import { useMutation } from '@tanstack/react-query';
import { cambioService } from '@/api/services/cambio.service';
import type {
  CambioResponse,
  ProcesarCambioRequest,
  ValidarEstadoProductoRequest,
  ValidarEstadoProductoResponse,
} from '@/types/api';

/** Parámetros para validar el estado físico dentro del flujo de cambio. */
interface ValidarEstadoProductoParams {
  cambioId: string;
  request: ValidarEstadoProductoRequest;
}

/**
 * Registra el cambio de un producto validando el plazo de 15 días (HU-02).
 *
 * El error queda como `unknown`; la página lo normaliza con
 * `normalizarErrorApi` (ej. PLAZO_VENCIDO).
 */
export function useRegistrarCambio() {
  return useMutation<CambioResponse, unknown, ProcesarCambioRequest>({
    mutationFn: (request) => cambioService.procesarCambio(request),
  });
}

/**
 * Valida el estado físico del producto presentado a cambio (HU-03).
 *
 * Errores esperados: CAMBIO_NO_ENCONTRADO (404),
 * PRODUCTO_NO_APTO y OBSERVACIONES_REQUERIDAS (422).
 */
export function useValidarEstadoProducto() {
  return useMutation<ValidarEstadoProductoResponse, unknown, ValidarEstadoProductoParams>(
    {
      mutationFn: ({ cambioId, request }) =>
        cambioService.validarEstadoProducto(cambioId, request),
    },
  );
}
