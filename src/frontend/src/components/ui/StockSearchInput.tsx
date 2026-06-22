import { forwardRef, type InputHTMLAttributes } from 'react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface StockSearchInputProps extends InputHTMLAttributes<HTMLInputElement> {
  /** Valor actual del input */
  value: string;
  /** Callback cuando cambia el valor */
  onChange: (value: string) => void;
  /** Callback cuando se presiona Enter */
  onSearch: (value: string) => void;
  /** Placeholder del input */
  placeholder?: string;
  /** Si está deshabilitado */
  disabled?: boolean;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Input de búsqueda para consultar stock.
 *
 * 🎯 Características:
 * - Búsqueda al presionar Enter
 * - Icono de búsqueda visual
 * - Hint "Enter para buscar"
 * - Accesible (ARIA labels)
 *
 * SRP: Solo maneja la UI del input, no la lógica de búsqueda.
 */
export const StockSearchInput = forwardRef<HTMLInputElement, StockSearchInputProps>(
  ({ value, onChange, onSearch, placeholder, disabled, className, ...props }, ref) => {
    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter' && value.trim()) {
        onSearch(value.trim());
      }
    };

    return (
      <div className={cn('relative', className)}>
        <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
          <svg
            className="h-5 w-5 text-slate-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>

        <input
          ref={ref}
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder={placeholder || 'Buscar por nombre o código...'}
          className={cn(
            'block w-full rounded-lg border border-slate-300 bg-white py-2.5 pl-10 pr-24',
            'text-sm text-slate-900 placeholder-slate-400',
            'focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20',
            'disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-500',
            'transition-colors duration-200',
          )}
          aria-label="Buscar producto por nombre o código"
          {...props}
        />

        <div className="absolute inset-y-0 right-0 flex items-center pr-3">
          <kbd
            className={cn(
              'hidden rounded border border-slate-300 bg-slate-100 px-1.5 py-0.5',
              'text-xs font-sans text-slate-500',
              'sm:inline-block',
            )}
          >
            Enter
          </kbd>
        </div>
      </div>
    );
  },
);

StockSearchInput.displayName = 'StockSearchInput';