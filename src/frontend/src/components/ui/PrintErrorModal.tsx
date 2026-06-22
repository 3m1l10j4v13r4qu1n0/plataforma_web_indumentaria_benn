import { useEffect } from 'react';
import { cn } from '@/utils/cn';

interface PrintErrorModalProps {
  /** Si el modal está visible */
  isOpen: boolean;
  /** Mensaje de error (opcional) */
  errorMessage?: string;
  /** Callback al reintentar impresión */
  onRetry: () => void;
  /** Callback al omitir impresión */
  onSkip: () => void;
  /** Callback al cancelar (cerrar modal sin acción) */
  onCancel: () => void;
}

/**
 * Modal de error de impresora con opciones de acción.
 *
 * 🎯 Opciones disponibles:
 * - Reintentar: Intenta imprimir nuevamente
 * - Omitir: Continúa sin imprimir (la venta ya fue procesada)
 * - Cancelar: Cierra el modal sin acción
 *
 * SRP: Solo presenta el modal y delega acciones al contenedor.
 */
export function PrintErrorModal({
  isOpen,
  errorMessage = 'No se pudo conectar con la impresora. Verifique que esté encendida y conectada.',
  onRetry,
  onSkip,
  onCancel,
}: PrintErrorModalProps) {
  // Cierre con tecla Escape (accesibilidad)
  useEffect(() => {
    if (!isOpen) return;
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onCancel();
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [isOpen, onCancel]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="print-error-title"
    >
      <div
        className={cn(
          'w-full max-w-md rounded-xl bg-white p-6 shadow-2xl',
          'animate-in fade-in zoom-in-95 duration-200',
        )}
      >
        {/* Icono de error */}
        <div className="mb-4 flex justify-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-rose-100">
            <svg
              className="h-8 w-8 text-rose-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"
              />
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01"
              />
            </svg>
          </div>
        </div>

        {/* Contenido */}
        <div className="text-center">
          <h2
            id="print-error-title"
            className="text-xl font-bold text-slate-900"
          >
            Error de Impresión
          </h2>
          <p className="mt-2 text-sm text-slate-600">{errorMessage}</p>

          {/* Información adicional */}
          <div className="mt-4 rounded-lg bg-slate-50 p-3 text-left text-xs text-slate-600">
            <p className="font-semibold">La venta fue procesada correctamente.</p>
            <p className="mt-1">
              Puede reintentar la impresión, omitirla por ahora o cancelar.
            </p>
          </div>

          {/* Botones de acción */}
          <div className="mt-6 space-y-2">
            <button
              type="button"
              onClick={onRetry}
              autoFocus
              className={cn(
                'w-full rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-medium text-white',
                'transition-colors hover:bg-brand-700',
                'focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2',
              )}
            >
              Reintentar Impresión
            </button>

            <button
              type="button"
              onClick={onSkip}
              className={cn(
                'w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-medium text-slate-700',
                'transition-colors hover:bg-slate-50',
                'focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2',
              )}
            >
              Omitir Impresión
            </button>

            <button
              type="button"
              onClick={onCancel}
              className={cn(
                'w-full rounded-lg px-4 py-2.5 text-sm font-medium text-slate-500',
                'transition-colors hover:text-slate-700',
                'focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2',
              )}
            >
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
