import { cn } from '@/utils/cn';
import type { EstadoImpresora } from '@/types/domain';

interface PrinterStatusIndicatorProps {
  /** Estado actual de la impresora */
  estado: EstadoImpresora;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Indicador visual del estado de la impresora.
 *
 * 🎨 Estados visuales:
 * - idle: gris, icono de impresora
 * - printing: azul animado, icono de impresora con animación
 * - success: verde, icono de check
 * - error: rojo, icono de alerta
 *
 * SRP: Solo presenta el estado, sin lógica de impresión.
 */
export function PrinterStatusIndicator({
  estado,
  className,
}: PrinterStatusIndicatorProps) {
  const config = {
    idle: {
      bg: 'bg-slate-100',
      text: 'text-slate-600',
      border: 'border-slate-300',
      label: 'Impresora lista',
      icon: <PrinterIcon />,
    },
    printing: {
      bg: 'bg-blue-50',
      text: 'text-blue-700',
      border: 'border-blue-300',
      label: 'Imprimiendo...',
      icon: <PrinterIcon className="animate-pulse" />,
    },
    success: {
      bg: 'bg-emerald-50',
      text: 'text-emerald-700',
      border: 'border-emerald-300',
      label: 'Impresión exitosa',
      icon: <CheckIcon />,
    },
    error: {
      bg: 'bg-rose-50',
      text: 'text-rose-700',
      border: 'border-rose-300',
      label: 'Error de impresora',
      icon: <AlertIcon />,
    },
  }[estado];

  return (
    <div
      className={cn(
        'inline-flex items-center gap-2 rounded-lg border px-3 py-2 text-sm font-medium',
        config.bg,
        config.text,
        config.border,
        className,
      )}
      role="status"
      aria-label={config.label}
    >
      <div className="h-5 w-5">{config.icon}</div>
      <span>{config.label}</span>
    </div>
  );
}

function PrinterIcon({ className }: { className?: string }) {
  return (
    <svg
      className={cn('h-5 w-5', className)}
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
    </svg>
  );
}

function CheckIcon() {
  return (
    <svg
      className="h-5 w-5"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2.5}
        d="M5 13l4 4L19 7"
      />
    </svg>
  );
}

function AlertIcon() {
  return (
    <svg
      className="h-5 w-5"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
      />
    </svg>
  );
}
