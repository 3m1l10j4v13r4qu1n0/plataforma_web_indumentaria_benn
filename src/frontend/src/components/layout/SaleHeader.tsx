import { cn } from '@/utils/cn';

interface SaleHeaderProps {
  /** Título de la pantalla */
  title: string;
  /** Nombre del cajero */
  cajero: string;
  /** Número de caja */
  caja: string;
  /** Fecha formateada (ej: "05 Jun 2026 - 14:30") */
  fecha: string;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Header de la pantalla de venta.
 *
 * 🎯 Alineado con el mockup HU-01:
 * - Título "Nueva Venta"
 * - "Cajero: Juan Pérez | Caja: 01"
 * - Fecha actual
 *
 * SRP: Solo presenta el header, sin lógica.
 */
export function SaleHeader({
  title,
  cajero,
  caja,
  fecha,
  className,
}: SaleHeaderProps) {
  return (
    <header
      className={cn(
        'mb-6 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between',
        className,
      )}
    >
      <div>
        <h1 className="text-2xl font-bold text-slate-900">{title}</h1>
        <p className="mt-1 text-sm text-slate-600">
          Cajero: <span className="font-medium">{cajero}</span>
          <span className="mx-2 text-slate-400">|</span>
          Caja: <span className="font-medium">{caja}</span>
        </p>
      </div>
      <div className="text-sm text-slate-500">
        <span className="font-medium">Fecha</span>
        <br />
        <time className="text-slate-700">{fecha}</time>
      </div>
    </header>
  );
}
