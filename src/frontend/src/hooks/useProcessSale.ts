import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ventaService } from '@/api/services/venta.service';
import { toVentaRequest, toVentaProcesada } from '@/types/api';
import { productSearchQueryKeys } from './useProductSearch';
import type { ItemCarrito, VentaProcesada } from '@/types/domain';

interface UseProcessSaleResult {
  /** Procesa la venta */
  processSale: (carrito: ItemCarrito[], vendedorId: string) => void;
  /** Venta procesada (si fue exitosa) */
  ventaProcesada: VentaProcesada | null;
  /** Estado de carga */
  isProcessing: boolean;
  /** Error de la petición */
  error: Error | null;
  /** Resetea el estado (después de mostrar confirmación) */
  reset: () => void;
}

/**
 * Hook que procesa una venta (mutation).
 *
 * 🎯 Responsabilidades (SRP):
 * - Enviar la venta al backend
 * - Invalidar cache de productos (para que se actualice el stock)
 * - Exponer estados de carga y error
 *
 * ❌ NO hace:
 * - Validación de stock (delegado a useCartValidation)
 * - Limpieza del carrito (delegado al contenedor)
 */
export function useProcessSale(): UseProcessSaleResult {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: ({ carrito, vendedorId }: { carrito: ItemCarrito[]; vendedorId: string }) => {
      const request = toVentaRequest(carrito, vendedorId);
      return ventaService.procesarVenta(request);
    },
    onSuccess: (response) => {
      // Invalida cache de búsqueda de productos para que se actualice el stock
      queryClient.invalidateQueries({ queryKey: productSearchQueryKeys.all });
      // Guarda la venta procesada
      mutation.data = response;
    },
  });

  const processSale = (carrito: ItemCarrito[], vendedorId: string) => {
    mutation.mutate({ carrito, vendedorId });
  };

  const ventaProcesada = mutation.data ? toVentaProcesada(mutation.data) : null;

  const reset = () => {
    mutation.reset();
  };

  return {
    processSale,
    ventaProcesada,
    isProcessing: mutation.isPending,
    error: mutation.error instanceof Error ? mutation.error : null,
    reset,
  };
}
