import { useState, useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import { productosService } from '@/api/services/productos.service';
import type { ProductoBusqueda } from '@/types/domain';

interface UseBuscarProductosResult {
  /** Término de búsqueda actual */
  query: string;
  /** Actualizar el término de búsqueda (no dispara la búsqueda) */
  setQuery: (value: string) => void;
  /** Disparar la búsqueda con el término actual */
  ejecutarBusqueda: () => void;
  /** Resultados de la búsqueda */
  resultados: ProductoBusqueda[];
  /** Total de productos encontrados */
  totalEncontrados: number;
  /** Mensaje del backend (ej. "No se encontraron productos...") */
  mensajeBackend?: string | null;
  /** Está cargando la búsqueda */
  isLoading: boolean;
  /** Error de la búsqueda */
  error: string | null;
  /** Indica si se ha realizado al menos una búsqueda */
  buscoAlMenosUnaVez: boolean;
}

/**
 * Hook que encapsula la lógica de búsqueda de productos (HU-06).
 *
 * SRP: Maneja estado de búsqueda + llamada al servicio.
 * La búsqueda se ejecuta solo cuando el usuario presiona Enter o llama a `ejecutarBusqueda`.
 */
export function useBuscarProductos(): UseBuscarProductosResult {
  const [inputValue, setInputValue] = useState('');
  const [activeQuery, setActiveQuery] = useState('');
  const [buscoAlMenosUnaVez, setBuscoAlMenosUnaVez] = useState(false);

  const ejecutarBusqueda = useCallback(() => {
    const trimmed = inputValue.trim();
    if (trimmed.length >= 3) {
      setActiveQuery(trimmed);
      setBuscoAlMenosUnaVez(true);
    }
  }, [inputValue]);

  const { data, isLoading, error } = useQuery({
    queryKey: ['buscar-productos', activeQuery],
    queryFn: () => productosService.buscarProductos(activeQuery),
    enabled: activeQuery.length >= 3,
    retry: false,
  });

  return {
    query: inputValue,
    setQuery: setInputValue,
    ejecutarBusqueda,
    resultados: data?.resultados ?? [],
    totalEncontrados: data?.totalEncontrados ?? 0,
    mensajeBackend: data?.mensaje ?? null,
    isLoading,
    error: error ? 'Ocurrió un error al buscar productos. Intentalo de nuevo.' : null,
    buscoAlMenosUnaVez,
  };
}
