import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface ResultsHeaderProps {
  /** Cantidad de resultados encontrados */
  count: number;
  /** Texto personalizado (opcional) */
  label?: string;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Header que muestra la cantidad de resultados de búsqueda.
 *
 * SRP: Solo renderiza el contador, sin lógica de filtrado.
 */
export function ResultsHeader({ count, label, className }: ResultsHeaderProps) {
  return (
    <div className={cn('flex items-center justify-between', className)}>
      <h2 className="text-sm font-medium text-slate-700">
        {label || 'Resultados encontrados'}
        <span className="ml-2 text-slate-500">({count})</span>
      </h2>
    </div>
  );
}