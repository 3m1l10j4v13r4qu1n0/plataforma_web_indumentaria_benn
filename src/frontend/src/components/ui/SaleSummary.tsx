import { cn } from '@/utils/cn';
import { formatCurrency } from '@/utils/formatCurrency';

interface SaleSummaryProps {
  /** Cantidad total de artículos en el carrito */
  totalArticulos: number;
  /** Monto total a pagar */
  totalPagar: number;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Resumen de la venta con total de artículos y monto a pagar.
 *
 * SRP: Solo presenta el resumen, sin cálculos.
 */
export function SaleSummary({
  totalArticulos,
  totalPagar,
  className,
}: SaleSummaryProps) {
  return (
    <div
      className={cn(
        'rounded-lg border border-slate-200 bg-white p-4 shadow-sm',
        className,
      )}
    >
      <dl className="space-y-3">
        <div className="flex items-center justify-between">
          <dt className="text-sm text-slate-600">Total de artículos</dt>
          <dd className="text-lg font-semibold text-slate-900">
            {totalArticulos}
          </dd>
        </div>
        <div className="border-t border-slate-200 pt-3">
          <div className="flex items-center justify-between">
            <dt className="text-base font-semibold text-slate-700">
              Total a Pagar
            </dt>
            <dd className="text-2xl font-bold text-brand-700">
              {formatCurrency(totalPagar)}
            </dd>
          </div>
        </div>
      </dl>
    </div>
  );
}
