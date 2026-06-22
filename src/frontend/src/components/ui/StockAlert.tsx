import { cn } from '@/utils/cn';

export interface StockAlertItem {
  /** Nombre del producto con problema */
  nombre: string;
  /** Motivo del error */
  motivo: 'SIN_STOCK' | 'CANTIDAD_EXCEDE_STOCK';
  /** Stock disponible (para el mensaje) */
  stockDisponible?: number;
}

interface StockAlertProps {
  /** Lista de productos con problemas de stock */
  items: StockAlertItem[];
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Alerta que muestra los productos con problemas de stock.
 *
 * 🎯 Alineada con el mockup HU-01:
 * - "No se puede procesar la venta"
 * - Mensaje específico por producto
 *
 * SRP: Solo presenta la alerta, sin lógica de validación.
 */
export function StockAlert({ items, className }: StockAlertProps) {
  if (items.length === 0) return null;

  return (
    <div
      className={cn(
        'rounded-lg border border-rose-200 bg-rose-50 p-4',
        className,
      )}
      role="alert"
      aria-live="assertive"
    >
      <div className="flex items-start gap-3">
        <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-rose-100">
          <svg
            className="h-4 w-4 text-rose-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
        </div>
        <div className="flex-1">
          <h3 className="text-sm font-semibold text-rose-900">
            No se puede procesar la venta
          </h3>
          <ul className="mt-1 space-y-1">
            {items.map((item) => (
              <li key={item.nombre} className="text-sm text-rose-700">
                {item.motivo === 'SIN_STOCK' ? (
                  <>
                    El producto <strong>"{item.nombre}"</strong> no tiene stock
                    disponible. Por favor, elimínalo del carrito para continuar.
                  </>
                ) : (
                  <>
                    El producto <strong>"{item.nombre}"</strong> solo tiene{' '}
                    <strong>{item.stockDisponible}</strong> unidades disponibles.
                    Ajusta la cantidad o elimínalo del carrito.
                  </>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
