import type { ReactNode } from 'react';
import { cn } from '@/utils/cn';

type AlertVariant = 'error' | 'success' | 'warning' | 'info';

interface AlertProps {
  /** Variante visual de la alerta */
  variant: AlertVariant;
  /** Mensaje principal de la alerta */
  message: string;
  /** Título opcional de la alerta */
  title?: string;
  /** Icono personalizado (opcional) */
  icon?: ReactNode;
  /** Clase CSS adicional */
  className?: string;
}

const variantClasses: Record<AlertVariant, string> = {
  error: 'border-rose-200 bg-rose-50 text-rose-800',
  success: 'border-emerald-200 bg-emerald-50 text-emerald-800',
  warning: 'border-amber-200 bg-amber-50 text-amber-800',
  info: 'border-sky-200 bg-sky-50 text-sky-800',
};

/**
 * Alerta reutilizable para mensajes de error, éxito, advertencia o info.
 *
 * SRP: Solo presenta el mensaje, sin lógica de negocio.
 */
export function Alert({ variant, title, message, icon, className }: AlertProps) {
  return (
    <div
      className={cn(
        'flex items-start gap-3 rounded-lg border px-4 py-3',
        variantClasses[variant],
        className,
      )}
      role={variant === 'error' ? 'alert' : 'status'}
      aria-live="polite"
    >
      {icon && <div className="mt-0.5 shrink-0">{icon}</div>}
      <div className="min-w-0">
        {title && <p className="text-sm font-semibold">{title}</p>}
        <p className="text-sm">{message}</p>
      </div>
    </div>
  );
}