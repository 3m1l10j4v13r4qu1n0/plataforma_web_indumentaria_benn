import { cn } from '@/utils/cn';

export type StockStatus = 'available' | 'low' | 'out';

interface StockIndicatorProps {
  /** Cantidad de stock disponible */
  quantity: number;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Indicador visual del stock disponible de un producto.
 *
 * 🎨 Estados visuales (alineados con mockup HU-01):
 * - available (verde): stock > 0 → "N disponibles"
 * - out (rojo): stock = 0 → "0 disponibles" (bloquea la venta)
 *
 * SRP: Solo renderiza el indicador, sin lógica de negocio.
 */
export function StockIndicator({ quantity, className }: StockIndicatorProps) {
  const status: StockStatus = quantity === 0 ? 'out' : 'available';

  const config = {
    available: {
      text: 'text-emerald-700',
      bg: 'bg-emerald-50',
      border: 'border-emerald-200',
    },
    low: {
      text: 'text-amber-700',
      bg: 'bg-amber-50',
      border: 'border-amber-200',
    },
    out: {
      text: 'text-rose-700',
      bg: 'bg-rose-50',
      border: 'border-rose-200',
    },
  }[status];

  return (
    <span
      className={cn(
        'inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium',
        config.bg,
        config.text,
        config.border,
        className,
      )}
      role="status"
      aria-label={`${quantity} unidades disponibles`}
    >
      {quantity} disponibles
    </span>
  );
}
