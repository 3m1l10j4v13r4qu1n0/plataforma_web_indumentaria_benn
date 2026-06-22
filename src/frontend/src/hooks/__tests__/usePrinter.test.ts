import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { usePrinter } from '@/hooks/usePrinter';

describe('usePrinter', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('inicializa con estado idle', () => {
    const { result } = renderHook(() => usePrinter());

    expect(result.current.estado).toBe('idle');
  });

  it('cambia a "printing" al llamar print()', () => {
    const { result } = renderHook(() => usePrinter({ printDuration: 1500 }));

    act(() => {
      result.current.print();
    });

    expect(result.current.estado).toBe('printing');
  });

  it('cambia a "success" después de la duración configurada', () => {
    const { result } = renderHook(() => usePrinter({ printDuration: 1500 }));

    act(() => {
      result.current.print();
    });

    expect(result.current.estado).toBe('printing');

    act(() => {
      vi.advanceTimersByTime(1500);
    });

    expect(result.current.estado).toBe('success');
  });

  it('cambia a "error" cuando forceError es true', () => {
    const { result } = renderHook(() =>
      usePrinter({ printDuration: 1500, forceError: true }),
    );

    act(() => {
      result.current.print();
    });

    act(() => {
      vi.advanceTimersByTime(1500);
    });

    expect(result.current.estado).toBe('error');
  });

  it('retry() reinicia el proceso de impresión', () => {
    const { result } = renderHook(() =>
      usePrinter({ printDuration: 1500, forceError: true }),
    );

    // Primer intento → error
    act(() => {
      result.current.print();
    });
    act(() => {
      vi.advanceTimersByTime(1500);
    });
    expect(result.current.estado).toBe('error');

    // Reintento (ahora con forceError=false por defecto)
    const { result: result2 } = renderHook(() =>
      usePrinter({ printDuration: 1500, forceError: false }),
    );

    act(() => {
      result2.current.retry();
    });
    expect(result2.current.estado).toBe('printing');

    act(() => {
      vi.advanceTimersByTime(1500);
    });
    expect(result2.current.estado).toBe('success');
  });

  it('skip() resetea el estado a idle', () => {
    const { result } = renderHook(() => usePrinter({ printDuration: 1500 }));

    act(() => {
      result.current.print();
    });
    expect(result.current.estado).toBe('printing');

    act(() => {
      result.current.skip();
    });
    expect(result.current.estado).toBe('idle');
  });

  it('reset() resetea el estado a idle', () => {
    const { result } = renderHook(() => usePrinter({ printDuration: 1500 }));

    act(() => {
      result.current.print();
    });
    act(() => {
      vi.advanceTimersByTime(1500);
    });
    expect(result.current.estado).toBe('success');

    act(() => {
      result.current.reset();
    });
    expect(result.current.estado).toBe('idle');
  });

  it('limpia el timer anterior si se llama print() mientras está printing', () => {
    const { result } = renderHook(() => usePrinter({ printDuration: 1500 }));

    act(() => {
      result.current.print();
    });

    // Avanza 1000ms (aún en printing)
    act(() => {
      vi.advanceTimersByTime(1000);
    });
    expect(result.current.estado).toBe('printing');

    // Llama print() de nuevo (reinicia el timer)
    act(() => {
      result.current.print();
    });

    // Avanza 500ms más (total 1500ms desde el primer print, pero el timer se reinició)
    act(() => {
      vi.advanceTimersByTime(500);
    });
    // Aún debe estar en printing porque el timer se reinició
    expect(result.current.estado).toBe('printing');

    // Avanza 1000ms más (total 1500ms desde el segundo print)
    act(() => {
      vi.advanceTimersByTime(1000);
    });
    expect(result.current.estado).toBe('success');
  });
});
