import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface PageHeaderProps {
  /** Título principal de la página */
  title: string;
  /** Subtítulo o descripción (opcional) */
  subtitle?: string;
  /** Información adicional (ej: nombre del usuario) */
  meta?: {
    label: string;
    value: string;
  };
  /** Fecha/hora actual (opcional) */
  timestamp?: string;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Header de página reutilizable.
 *
 * SRP: Solo presenta el header, sin lógica de navegación.
 */
export function PageHeader({
  title,
  subtitle,
  meta,
  timestamp,
  className,
}: PageHeaderProps) {
  return (
    <header className={cn('mb-6', className)}>
      <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">{title}</h1>
          {subtitle && <p className="mt-1 text-sm text-slate-600">{subtitle}</p>}
        </div>

        {(meta || timestamp) && (
          <div className="mt-2 sm:mt-0">
            {meta && (
              <p className="text-sm text-slate-600">
                <span className="font-medium">{meta.label}:</span> {meta.value}
              </p>
            )}
            {timestamp && <p className="text-xs text-slate-500">{timestamp}</p>}
          </div>
        )}
      </div>
    </header>
  );
}