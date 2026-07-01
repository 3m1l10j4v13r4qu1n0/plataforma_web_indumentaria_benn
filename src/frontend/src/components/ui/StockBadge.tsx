import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Utilidad para combinar clases de Tailwind de forma segura.
 * DRY: Evita duplicación de lógica de merge de clases.
 */
function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export type StockLevel = 'healthy' | 'low' | 'out';

interface StockBadgeProps {
  /** Nivel de stock del producto */
  level: StockLevel;
  /** Cantidad de stock actual */
  quantity: number;
  /** Clase CSS adicional (opcional) */
  className?: string;
}

/**
 * Badge visual que indica el nivel de stock de un producto.
 *
 * 🎨 Estados visuales:
 * - healthy (verde): Stock >= stock mínimo
 * - low (amarillo): 0 < stock < stock mínimo
 * - out (rojo): stock = 0
 *
 * SRP: Solo renderiza el badge, sin lógica de negocio.
 */
export function StockBadge({ level, quantity, className }: StockBadgeProps) {
  const config = {
    healthy: {
      bg: 'bg-emerald-100',
      text: 'text-emerald-800',
      border: 'border-emerald-200',
      label: 'en stock',
    },
    low: {
      bg: 'bg-amber-100',
      text: 'text-amber-800',
      border: 'border-amber-200',
      label: 'stock bajo',
    },
    out: {
      bg: 'bg-rose-100',
      text: 'text-rose-800',
      border: 'border-rose-200',
      label: 'agotado',
    },
  }[level];

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium',
        config.bg,
        config.text,
        config.border,
        className,
      )}
      role="status"
      aria-label={`Stock: ${quantity} unidades - ${config.label}`}
    >
      <span
        className={cn(
          'h-1.5 w-1.5 rounded-full',
          level === 'healthy' && 'bg-emerald-600',
          level === 'low' && 'bg-amber-600',
          level === 'out' && 'bg-rose-600',
        )}
      />
      {quantity} {config.label}
    </span>
  );
}