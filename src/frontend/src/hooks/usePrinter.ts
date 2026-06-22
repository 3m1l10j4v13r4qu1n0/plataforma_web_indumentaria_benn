import { useState, useCallback, useRef } from 'react';
import type { EstadoImpresora } from '@/types/domain';

interface UsePrinterOptions {
  /** Duración de la simulación de impresión en milisegundos (default: 1500) */
  printDuration?: number;
  /** Forzar error de impresión (para testing, default: false) */
  forceError?: boolean;
}

interface UsePrinterResult {
  /** Estado actual de la impresora */
  estado: EstadoImpresora;
  /** Inicia el proceso de impresión */
  print: () => void;
  /** Reintenta la impresión (después de error) */
  retry: () => void;
  /** Omite la impresión y continúa */
  skip: () => void;
  /** Resetea el estado a idle */
  reset: () => void;
}

/**
 * Hook que simula el proceso de impresión de un ticket.
 *
 * 🎯 Responsabilidades (SRP):
 * - Manejar estados de impresión (idle, printing, success, error)
 * - Simular delay de impresión (1.5 segundos por defecto)
 * - Permitir reintentar, omitir o resetear
 *
 * ⚠️ NOTA: Esta es una simulación visual. No implementa impresión real
 * (window.print() o conexión a impresora física) por YAGNI.
 *
 * 🧪 Para testing: usar `forceError: true` para simular fallos.
 */
export function usePrinter(options: UsePrinterOptions = {}): UsePrinterResult {
  const { printDuration = 1500, forceError = false } = options;
  const [estado, setEstado] = useState<EstadoImpresora>('idle');
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const print = useCallback(() => {
    // Limpia cualquier timer previo
    if (timerRef.current) {
      clearTimeout(timerRef.current);
    }

    setEstado('printing');

    // Simula el proceso de impresión
    timerRef.current = setTimeout(() => {
      setEstado(forceError ? 'error' : 'success');
    }, printDuration);
  }, [printDuration, forceError]);

  const retry = useCallback(() => {
    print();
  }, [print]);

  const skip = useCallback(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
    }
    setEstado('idle');
  }, []);

  const reset = useCallback(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
    }
    setEstado('idle');
  }, []);

  return {
    estado,
    print,
    retry,
    skip,
    reset,
  };
}
