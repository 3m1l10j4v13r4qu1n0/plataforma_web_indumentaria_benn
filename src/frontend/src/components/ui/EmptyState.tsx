import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface EmptyStateProps {
  /** Título del estado vacío */
  title?: string;
  /** Descripción del estado vacío */
  description?: string;
  /** Icono personalizado (opcional) */
  icon?: React.ReactNode;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Estado vacío para mostrar cuando no hay resultados.
 *
 * SRP: Solo presenta el estado vacío, sin lógica.
 */
export function EmptyState({
  title = 'No se encontraron resultados',
  description = 'Intenta buscar con otro nombre o código de producto',
  icon,
  className,
}: EmptyStateProps) {
  const defaultIcon = (
    <svg
      className="h-12 w-12 text-slate-300"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={1.5}
        d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
      />
    </svg>
  );

  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center rounded-lg border border-dashed border-slate-300 bg-slate-50 py-12 px-4',
        className,
      )}
      role="status"
      aria-live="polite"
    >
      <div className="mb-4">{icon || defaultIcon}</div>
      <h3 className="text-sm font-medium text-slate-900">{title}</h3>
      <p className="mt-1 text-center text-sm text-slate-500">{description}</p>
    </div>
  );
}