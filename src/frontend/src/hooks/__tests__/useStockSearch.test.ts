import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useStockSearch } from '@/hooks/useStockSearch';

describe('useStockSearch', () => {
  it('inicializa con query y confirmedQuery vacíos', () => {
    const { result } = renderHook(() => useStockSearch());

    expect(result.current.query).toBe('');
    expect(result.current.confirmedQuery).toBe('');
  });

  it('setQuery actualiza solo el input, NO el confirmedQuery', () => {
    const { result } = renderHook(() => useStockSearch());

    act(() => {
      result.current.setQuery('camiseta');
    });

    expect(result.current.query).toBe('camiseta');
    expect(result.current.confirmedQuery).toBe(''); // Aún no confirmado
  });

  it('confirmSearch actualiza confirmedQuery con el valor trimmeado', () => {
    const { result } = renderHook(() => useStockSearch());

    act(() => {
      result.current.setQuery('  camiseta  ');
      result.current.confirmSearch('  camiseta  ');
    });

    expect(result.current.confirmedQuery).toBe('camiseta');
  });

  it('clearSearch resetea ambos valores', () => {
    const { result } = renderHook(() => useStockSearch());

    act(() => {
      result.current.setQuery('camiseta');
      result.current.confirmSearch('camiseta');
    });

    act(() => {
      result.current.clearSearch();
    });

    expect(result.current.query).toBe('');
    expect(result.current.confirmedQuery).toBe('');
  });
});