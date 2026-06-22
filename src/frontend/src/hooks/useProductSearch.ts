import { useQuery } from '@tanstack/react-query';
import { productosService } from '@/api/services/productos.service';
import type { ProductoBusquedaItem } from '@/types/api';

/**
 * Query key factory para búsqueda de productos.
 * DRY: Centraliza las claves de cache de TanStack Query.
 */
export const productSearchQueryKeys = {
  all: ['productSearch'] as const,
  byQuery: (query: string) => [...productSearchQueryKeys.all, query] as const,
};

interface UseProductSearchResult {
  /** Producto encontrado (si existe y es único) */
  producto: ProductoBusquedaItem | null;
  /** Mensaje del backend */
  mensaje: string;
  /** Estado de carga */
  isLoading: boolean;
  /** Error de la petición */
  error: Error | null;
  /** Si la búsqueda fue ejecutada */
  hasSearched: boolean;
}

/**
 * Hook que busca un producto por código o nombre.
 *
 * 🎯 Casos de uso:
 * - HU-01: Buscar producto para agregar al carrito
 * - HU-06: Búsqueda general de stock
 *
 * SRP: Solo maneja el estado de la búsqueda, no la UI.
 *
 * @param query - Texto de búsqueda (código exacto o fragmento de nombre)
 */
export function useProductSearch(query: string): UseProductSearchResult {
  const trimmedQuery = query.trim();
  const hasSearched = trimmedQuery.length >= 2; // Backend requiere min_length=2

  const { data, isLoading, error } = useQuery({
    queryKey: productSearchQueryKeys.byQuery(trimmedQuery),
    queryFn: () => productosService.buscarProductos({ query: trimmedQuery }),
    enabled: hasSearched,
    staleTime: 10_000, // 10 segundos de cache fresco
  });

  // Si hay exactamente 1 resultado, lo devolvemos
  const producto = data?.productos.length === 1 ? data.productos[0] : null;
  const mensaje = data?.mensaje ?? '';

  return {
    producto,
    mensaje,
    isLoading,
    error: error instanceof Error ? error : null,
    hasSearched,
  };
}
