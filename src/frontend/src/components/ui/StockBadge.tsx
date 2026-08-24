import { cn } from '@/utils/cn';
import type { NivelStock } from '@/constants/stock';

export type { NivelStock } from '@/constants/stock';

/** Formato textual del badge según la pantalla del contrato. */
export type StockBadgeFormato = 'en-stock' | 'disponibles';

interface StockBadgeProps {
  /** Nivel de stock del producto */
  level: NivelStock;
  /** Cantidad de stock actual */
  quantity: number;
  /**
   * Formato del texto:
   * - `en-stock`: `{n} en stock` (HU-06 Consulta de stock).
   * - `disponibles`: `{n} disponibles` (HU-01 Nueva venta).
   */
  formato?: StockBadgeFormato;
  /** Clase CSS adicional (opcional) */
  className?: string;
}

const PALETA_NIVEL: Record<
  NivelStock,
  { bg: string; text: string; border: string; dot: string }
> = {
  healthy: {
    bg: 'bg-green-100',
    text: 'text-green-800',
    border: 'border-green-200',
    dot: 'bg-green-600',
  },
  low: {
    bg: 'bg-yellow-100',
    text: 'text-yellow-800',
    border: 'border-yellow-200',
    dot: 'bg-yellow-600',
  },
  out: {
    bg: 'bg-red-100',
    text: 'text-red-800',
    border: 'border-red-200',
    dot: 'bg-red-600',
  },
};

/**
 * Badge visual que indica el nivel de stock de un producto.
 *
 * 🎨 Estados visuales del contrato:
 * - healthy (verde): stock disponible
 * - low (amarillo): stock bajo el umbral
 * - out (rojo): agotado
 *
 * SRP: Solo renderiza el badge, sin lógica de negocio.
 */
export function StockBadge({
  level,
  quantity,
  formato = 'en-stock',
  className,
}: StockBadgeProps) {
  const paleta = PALETA_NIVEL[level];
  const label = construirLabel(level, quantity, formato);

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium',
        paleta.bg,
        paleta.text,
        paleta.border,
        className,
      )}
      role="status"
      aria-label={`Stock: ${quantity} unidades - ${label}`}
    >
      <span className={cn('h-1.5 w-1.5 rounded-full', paleta.dot)} />
      {label}
    </span>
  );
}

/**
 * Construye el texto del badge según nivel y formato contractual.
 */
function construirLabel(
  level: NivelStock,
  quantity: number,
  formato: StockBadgeFormato,
): string {
  if (level === 'out' && formato === 'en-stock') {
    return 'Agotado';
  }
  const sufijo = formato === 'disponibles' ? 'disponibles' : 'en stock';
  return `${quantity} ${sufijo}`;
}
