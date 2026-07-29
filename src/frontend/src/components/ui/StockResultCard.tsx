import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { StockBadge, type StockLevel } from './StockBadge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export interface StockResultCardProps {
  /** Código del producto */
  codigo: string;
  /** Nombre del producto */
  nombre: string;
  /** Categoría del producto */
  categoria: string;
  /** Stock actual */
  stockActual: number;
  /** Stock mínimo */
  stockMinimo: number;
  /** Fecha de última actualización (ISO string) */
  updatedAt: string;
  /** Texto relativo de última actualización (ej: "hace 2 min") */
  lastUpdateRelative: string;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Tarjeta que muestra la información de stock de un producto.
 *
 * 📋 Información mostrada:
 * - Nombre del producto
 * - Código y categoría
 * - Nivel de stock con badge visual
 * - Última actualización
 *
 * SRP: Solo presenta datos, sin lógica de negocio.
 */
export function StockResultCard({
  codigo,
  nombre,
  categoria,
  stockActual,
  stockMinimo,
  updatedAt,
  lastUpdateRelative,
  className,
}: StockResultCardProps) {
  // Determinar el nivel de stock (lógica visual simple, KISS)
  const stockLevel: StockLevel = stockActual === 0 ? 'out' : stockActual < stockMinimo ? 'low' : 'healthy';

  return (
    <article
      className={cn(
        'rounded-lg border border-slate-200 bg-white p-4 shadow-sm',
        'transition-shadow duration-200 hover:shadow-md',
        className,
      )}
    >
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        {/* Información principal */}
        <div className="flex-1">
          <h3 className="text-base font-semibold text-slate-900">{nombre}</h3>
          <p className="mt-1 text-sm text-slate-600">
            Código: <span className="font-mono font-medium">{codigo}</span>
            <span className="mx-2 text-slate-400">|</span>
            Categoría: <span className="font-medium">{categoria}</span>
          </p>
        </div>

        {/* Badge de stock */}
        <div className="flex items-center">
          <StockBadge level={stockLevel} quantity={stockActual} />
        </div>
      </div>

      {/* Última actualización */}
      <div className="mt-3 flex items-center gap-2 text-xs text-slate-500">
        <svg
          className="h-3.5 w-3.5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <time dateTime={updatedAt} title={new Date(updatedAt).toLocaleString()}>
          Última actualización: {lastUpdateRelative}
        </time>
      </div>
    </article>
  );
}