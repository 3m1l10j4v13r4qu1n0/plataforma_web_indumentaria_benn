import { useEffect } from 'react';
import { cn } from '@/utils/cn';

type ToastVariant = 'success' | 'error' | 'info';

interface ToastProps {
  /** Mensaje a mostrar */
  message: string;
  /** Variante visual (default: success) */
  variant?: ToastVariant;
  /** Milisegundos hasta auto-descartarse (default: 5000) */
  duration?: number;
  /** Callback al cerrar (auto-dismiss o botón) */
  onDismiss: () => void;
  /** Clase CSS adicional */
  className?: string;
}

const VARIANTES: Record<ToastVariant, string> = {
  success: 'border-green-500 bg-green-50 text-green-800',
  error: 'border-red-500 bg-red-50 text-red-800',
  info: 'border-brand-500 bg-brand-50 text-brand-800',
};

/**
 * Notificación flotante tipo "Toast" con auto-dismiss (requisito HU-08:
 * confirmación de éxito verde "Operación exitosa. Inventario actualizado").
 *
 * SRP: Solo presenta la notificación; el disparo queda en el contenedor.
 */
export function Toast({
  message,
  variant = 'success',
  duration = 5000,
  onDismiss,
  className,
}: ToastProps) {
  useEffect(() => {
    const timer = setTimeout(onDismiss, duration);
    return () => clearTimeout(timer);
  }, [duration, onDismiss]);

  return (
    <div
      role="status"
      aria-live="polite"
      className={cn(
        'fixed bottom-4 right-4 z-50 flex max-w-sm items-start gap-3 rounded-lg border-l-4 p-4 shadow-lg',
        VARIANTES[variant],
        className,
      )}
    >
      <svg
        className="mt-0.5 h-5 w-5 shrink-0"
        fill="none"
        stroke="currentColor"
        strokeWidth={2}
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
      </svg>
      <p className="text-sm font-medium">{message}</p>
      <button
        type="button"
        onClick={onDismiss}
        aria-label="Cerrar notificación"
        className="ml-auto shrink-0 text-current/60 hover:text-current"
      >
        <svg
          className="h-4 w-4"
          fill="none"
          stroke="currentColor"
          strokeWidth={2}
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  );
}
