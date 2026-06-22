import { useQuery } from '@tanstack/react-query';
import { productosService } from '@/api/services/productos.service';
import { toStockProducto } from '@/types/api';
import type { StockProducto } from '@/types/domain';

/**
 * Query key factory para productos.
 * DRY: Centraliza las claves de cache de TanStack Query.
 */
export const productosQueryKeys = {
  all: ['productos'] as const,
  busqueda: (query: string) => [...productosQueryKeys.all, 'busqueda', query] as const,
};

interface UseBuscarProductosResult {
  /** Lista de productos mapeados al dominio */
  productos: StockProducto[];
  /** Total de resultados (para paginación futura) */
  total: number;
  /** Estado de carga inicial */
  isLoading: boolean;
  /** Estado de refetch (cuando ya hay datos en cache) */
  isFetching: boolean;
  /** Error de la petición (si existe) */
  error: Error | null;
  /** Si la búsqueda fue ejecutada (query no vacío) */
  hasSearched: boolean;
}

/**
 * Hook que encapsula la búsqueda de productos con TanStack Query.
 *
 * SRP: Solo maneja el estado de la búsqueda (loading, error, data).
 *      No sabe de UI ni de formularios.
 *
 * 🎯 Características:
 * - Cache automático por query string
 * - Deduplicación de peticiones simultáneas
 * - Estados de carga y error tipados
 * - No ejecuta la búsqueda si el query está vacío (enabled: false)
 *
 * @param query - Texto de búsqueda (nombre o código)
 */
export function useBuscarProductos(query: string): UseBuscarProductosResult {
  const trimmedQuery = query.trim();
  const hasSearched = trimmedQuery.length > 0;

  const { data, isLoading, isFetching, error } = useQuery({
    queryKey: productosQueryKeys.busqueda(trimmedQuery),
    queryFn: () => productosService.buscarProductos({ query: trimmedQuery }),
    enabled: hasSearched, // Solo ejecuta si hay query
    staleTime: 30_000, // 30 segundos de cache fresco
    placeholderData: (previousData) => previousData, // Mantiene datos anteriores al refetch
  });

  const productos = (data?.productos ?? []).map(toStockProducto);
  const total = data?.total ?? 0;

  return {
    productos,
    total,
    isLoading,
    isFetching,
    error: error instanceof Error ? error : null,
    hasSearched,
  };
}