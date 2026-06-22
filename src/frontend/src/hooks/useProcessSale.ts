import { useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { ventaService } from '@/api/services/venta.service';
import { toVentaRequest, toVentaProcesada } from '@/types/api';
import type { ApiErrorResponse } from '@/types/api/error.types';
import { productSearchQueryKeys } from './useProductSearch';
import type { ItemCarrito, VentaProcesada } from '@/types/domain';

interface UseProcessSaleResult {
  /** Procesa la venta */
  processSale: (carrito: ItemCarrito[], vendedorId: string) => void;
  /** Venta procesada (si fue exitosa) */
  ventaProcesada: VentaProcesada | null;
  /** Estado de carga */
  isProcessing: boolean;
  /** Error estructurado con mensaje amigable */
  error: { code: string; message: string } | null;
  /** Resetea el estado (después de mostrar confirmación) */
  reset: () => void;
}

/**
 * Hook que procesa una venta (mutation).
 *
 * 🎯 Responsabilidades (SRP):
 * - Enviar la venta al backend
 * - Invalidar cache de productos (para que se actualice el stock)
 * - Extraer mensajes de error amigables del backend
 *
 * ⚠️ Manejo centralizado de errores:
 * - Extrae el mensaje del backend (ej: "El producto X no tiene stock...")
 * - NO usa try/catch dispersos
 */
export function useProcessSale(): UseProcessSaleResult {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: ({ carrito, vendedorId }: { carrito: ItemCarrito[]; vendedorId: string }) => {
      const request = toVentaRequest(carrito, vendedorId);
      return ventaService.procesarVenta(request);
    },
    onSuccess: () => {
      // Invalida cache de búsqueda de productos para que se actualice el stock
      queryClient.invalidateQueries({ queryKey: productSearchQueryKeys.all });
    },
  });

  const processSale = (carrito: ItemCarrito[], vendedorId: string) => {
    mutation.mutate({ carrito, vendedorId });
  };

  const ventaProcesada = mutation.data ? toVentaProcesada(mutation.data) : null;

  // Extraer error estructurado del backend
  const error = (() => {
    if (!mutation.error) return null;

    if (axios.isAxiosError(mutation.error) && mutation.error.response) {
      const apiError = mutation.error.response.data as ApiErrorResponse;
      return {
        code: apiError?.error ?? 'ERROR_DESCONOCIDO',
        message: apiError?.mensaje ?? mutation.error.message,
      };
    }

    return {
      code: 'ERROR_INTERNO',
      message: mutation.error instanceof Error ? mutation.error.message : 'Error desconocido',
    };
  })();

  const reset = () => {
    mutation.reset();
  };

  return {
    processSale,
    ventaProcesada,
    isProcessing: mutation.isPending,
    error,
    reset,
  };
}
