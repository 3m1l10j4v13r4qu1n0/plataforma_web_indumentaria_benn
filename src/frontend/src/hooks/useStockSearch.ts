import { useState, useCallback } from 'react';

interface UseStockSearchResult {
  /** Valor actual del input de búsqueda */
  query: string;
  /** Query confirmado (el que se envía a la API) */
  confirmedQuery: string;
  /** Actualiza el valor del input (sin disparar búsqueda) */
  setQuery: (value: string) => void;
  /** Confirma la búsqueda (dispara la petición a la API) */
  confirmSearch: (value: string) => void;
  /** Limpia el input y el query confirmado */
  clearSearch: () => void;
}

/**
 * Hook que maneja el estado local de la búsqueda de stock.
 *
 * SRP: Separa el estado del input (cambia con cada tecla)
 *      del query confirmado (solo cambia al presionar Enter).
 *
 * 🎯 Patrón: "Search on Enter"
 * - El usuario escribe libremente en el input
 * - La búsqueda a la API solo se dispara al confirmar (Enter)
 * - Evita peticiones innecesarias en cada cambio de tecla
 */
export function useStockSearch(): UseStockSearchResult {
  const [query, setQuery] = useState('');
  const [confirmedQuery, setConfirmedQuery] = useState('');

  const confirmSearch = useCallback((value: string) => {
    const trimmed = value.trim();
    setConfirmedQuery(trimmed);
  }, []);

  const clearSearch = useCallback(() => {
    setQuery('');
    setConfirmedQuery('');
  }, []);

  return {
    query,
    confirmedQuery,
    setQuery,
    confirmSearch,
    clearSearch,
  };
}