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
  error: 'border-red-500 bg-red-50 text-red-800',
  success: 'border-green-500 bg-green-50 text-green-800',
  warning: 'border-orange-500 bg-orange-50 text-orange-800',
  info: 'border-brand-500 bg-brand-50 text-brand-800',
};

/**
 * Alerta reutilizable para mensajes de error, éxito, advertencia o info.
 *
 * Sigue el patrón visual del contrato (docs/05_mockups/): borde izquierdo
 * grueso (`border-l-4`) + fondo tenue de la paleta funcional.
 *
 * SRP: Solo presenta el mensaje, sin lógica de negocio.
 */
export function Alert({ variant, title, message, icon, className }: AlertProps) {
  return (
    <div
      className={cn(
        'flex items-start gap-3 rounded-lg border-l-4 px-4 py-3',
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