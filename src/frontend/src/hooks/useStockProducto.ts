import { useQuery } from '@tanstack/react-query';
import { productosService } from '@/api/services/productos.service';
import type { StockProducto } from '@/types/domain';

/**
 * Consulta el stock de un producto por su código (HU-01).
 *
 * Solo se dispara cuando `codigo` tiene valor.
 */
export function useStockProducto(codigo: string) {
  return useQuery<StockProducto>({
    queryKey: ['stock-producto', codigo],
    queryFn: () => productosService.obtenerStock(codigo),
    enabled: codigo.trim().length > 0,
    retry: false,
  });
}