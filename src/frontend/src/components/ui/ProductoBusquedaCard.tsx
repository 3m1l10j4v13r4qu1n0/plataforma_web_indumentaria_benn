import type { ProductoBusqueda } from '@/types/domain';
import { cn } from '@/utils/cn';
import { StockBadge, type StockLevel } from './StockBadge';

interface ProductoBusquedaCardProps {
  producto: ProductoBusqueda;
  className?: string;
}

/**
 * Tarjeta que muestra un producto resultante de una búsqueda (HU-06).
 *
 * SRP: Solo presenta datos del resultado de búsqueda, sin lógica de negocio.
 */
export function ProductoBusquedaCard({ producto, className }: ProductoBusquedaCardProps) {
  const stockLevel: StockLevel =
    producto.stockActual === 0 ? 'out' : 'healthy';

  return (
    <article
      className={cn(
        'rounded-lg border border-slate-200 bg-white p-4 shadow-sm',
        'transition-shadow duration-200 hover:shadow-md',
        className,
      )}
    >
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex-1">
          <h3 className="text-base font-semibold text-slate-900">
            {producto.nombre}
          </h3>
          <p className="mt-1 text-sm text-slate-600">
            Código: <span className="font-mono font-medium">{producto.codigo}</span>
            <span className="mx-2 text-slate-400">|</span>
            Estado: <span className="font-medium">{producto.estado}</span>
          </p>
        </div>

        <div className="flex items-center">
          <StockBadge level={stockLevel} quantity={producto.stockActual} />
        </div>
      </div>
    </article>
  );
}
