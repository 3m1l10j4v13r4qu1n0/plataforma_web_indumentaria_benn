import type { ButtonHTMLAttributes, ReactNode } from 'react';
import { cn } from '@/utils/cn';

type ButtonVariant = 'primary' | 'secondary' | 'danger';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Variante visual del botón */
  variant?: ButtonVariant;
  /** Contenido del botón */
  children: ReactNode;
}

const variantClasses: Record<ButtonVariant, string> = {
  primary:
    'bg-brand-600 text-white hover:bg-brand-700 focus:ring-brand-500/40',
  secondary:
    'border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 focus:ring-slate-400/40',
  danger: 'bg-rose-600 text-white hover:bg-rose-700 focus:ring-rose-500/40',
};

/**
 * Botón reutilizable.
 *
 * SRP: Solo presenta el botón; la lógica de habilitado/disabled
 * (ej. sin stock) la decide el contenedor.
 */
export function Button({
  variant = 'primary',
  className,
  children,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2',
        'text-sm font-medium transition-colors duration-200',
        'focus:outline-none focus:ring-2',
        'disabled:cursor-not-allowed disabled:opacity-50',
        variantClasses[variant],
        className,
      )}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}