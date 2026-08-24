import type { ProductoBusqueda } from '@/types/domain';
import { cn } from '@/utils/cn';
import { calcularNivelStock } from '@/constants/stock';
import { StockBadge } from './StockBadge';

interface ProductoBusquedaCardProps {
  producto: ProductoBusqueda;
  className?: string;
}

/**
 * Tarjeta que muestra un producto resultante de una búsqueda (HU-06),
 * según el contrato visual (docs/05_mockups/mockup_hu06.html): icono de
 * categoría, nombre, metadatos y badge de stock a la derecha.
 *
 * La API de búsqueda no expone categoría ni fecha de actualización, por lo
 * que se muestra `Estado` (decisión D-005) y se omite el timestamp (D-004).
 *
 * SRP: Solo presenta datos del resultado de búsqueda, sin lógica de negocio.
 */
export function ProductoBusquedaCard({ producto, className }: ProductoBusquedaCardProps) {
  const nivelStock = calcularNivelStock(producto.stockActual);

  return (
    <article
      className={cn(
        'rounded-lg border border-slate-200 bg-white p-4 shadow-sm',
        'transition-shadow duration-200 hover:shadow-md',
        className,
      )}
    >
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-start gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-brand-50 text-brand-600">
            <svg
              className="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
              />
            </svg>
          </div>

          <div>
            <h3 className="text-base font-semibold text-slate-900">
              {producto.nombre}
            </h3>
            <p className="mt-1 text-sm text-slate-600">
              Código: <span className="font-mono font-medium">{producto.codigo}</span>
              <span className="mx-2 text-slate-400">|</span>
              Estado: <span className="font-medium">{producto.estado}</span>
            </p>
          </div>
        </div>

        <div className="flex shrink-0 items-center pl-13 sm:pl-0">
          <StockBadge level={nivelStock} quantity={producto.stockActual} />
        </div>
      </div>
    </article>
  );
}
