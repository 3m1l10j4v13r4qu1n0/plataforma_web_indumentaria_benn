import { cn } from '@/utils/cn';

interface PageHeaderProps {
  /** Título principal de la página */
  title: string;
  /** Subtítulo o descripción (opcional) */
  subtitle?: string;
  /** Contexto del usuario (ej: { label: 'Vendedor', value: 'V-001' }) */
  meta?: {
    label: string;
    value: string;
  };
  /** Fecha/hora actual formateada (opcional) */
  timestamp?: string;
  /** Etiqueta del timestamp en la cabecera (default: 'Sistema') */
  timestampLabel?: string;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Header de página reutilizable según el contrato visual
 * (docs/05_mockups/): banda de color de marca con título y contexto del
 * usuario a la izquierda, fecha del sistema a la derecha.
 *
 * SRP: Solo presenta el header, sin lógica de navegación.
 */
export function PageHeader({
  title,
  subtitle,
  meta,
  timestamp,
  timestampLabel = 'Sistema',
  className,
}: PageHeaderProps) {
  return (
    <header
      className={cn(
        'mb-6 flex flex-col gap-3 rounded-xl bg-brand-700 px-6 py-5 text-white sm:flex-row sm:items-center sm:justify-between',
        className,
      )}
    >
      <div>
        <h1 className="text-xl font-bold">{title}</h1>
        {subtitle && <p className="mt-1 text-sm text-brand-100">{subtitle}</p>}
        {meta && (
          <p className="mt-1 text-sm text-brand-100">
            <span className="font-medium text-white">{meta.label}:</span>{' '}
            {meta.value}
          </p>
        )}
      </div>

      {timestamp && (
        <div className="sm:text-right">
          <p className="text-xs uppercase tracking-wide text-brand-200">
            {timestampLabel}
          </p>
          <p className="text-sm font-semibold">{timestamp}</p>
        </div>
      )}
    </header>
  );
}
