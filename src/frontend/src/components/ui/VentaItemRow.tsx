import { cn } from '@/utils/cn';
import { Button } from './Button';
import { StockBadge, type NivelStock } from './StockBadge';
import { calcularNivelStock } from '@/constants/stock';
import { formatoMoneda } from '@/utils/format';

export interface VentaItem {
  productoId: string;
  nombre: string;
  precio: number;
  cantidad: number;
  /** Stock vigente al momento de agregar el ítem (contrato HU-01) */
  stockActual: number;
}

interface VentaItemRowProps {
  /** Item del carrito de la venta */
  item: VentaItem;
  /** Callback cuando cambia la cantidad inline */
  onCantidadChange: (cantidad: number) => void;
  /** Callback para quitar el item de la venta */
  onQuitar: () => void;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Fila de la tabla "Productos a vender" (HU-01) según el contrato visual:
 * Producto · Precio Unit. · Stock Actual · Cantidad · Subtotal.
 *
 * Cuando el ítem no tiene stock, la fila completa se resalta en rojo
 * (estado bloqueado del contrato).
 *
 * SRP: Solo presenta el item y emite callbacks, sin lógica de negocio.
 */
export function VentaItemRow({
  item,
  onCantidadChange,
  onQuitar,
  className,
}: VentaItemRowProps) {
  const sinStock = item.stockActual === 0;
  const nivelStock: NivelStock = calcularNivelStock(item.stockActual);
  const subtotal = item.precio * item.cantidad;

  return (
    <tr className={cn(sinStock && 'bg-red-50', className)}>
      <td className="px-4 py-3">
        <p
          className={cn(
            'text-sm font-medium',
            sinStock ? 'text-red-900' : 'text-slate-900',
          )}
        >
          {item.nombre}
        </p>
        <p
          className={cn(
            'font-mono text-xs',
            sinStock ? 'text-red-600' : 'text-slate-500',
          )}
        >
          SKU: {item.productoId}
        </p>
      </td>

      <td
        className={cn(
          'px-4 py-3 text-sm whitespace-nowrap',
          sinStock ? 'text-red-700' : 'text-slate-600',
        )}
      >
        {formatoMoneda(item.precio)}
      </td>

      <td className="px-4 py-3">
        <StockBadge
          level={nivelStock}
          quantity={item.stockActual}
          formato="disponibles"
        />
      </td>

      <td className="px-4 py-3">
        <input
          type="number"
          min={1}
          max={item.stockActual || 1}
          value={sinStock ? 0 : item.cantidad}
          onChange={(e) => onCantidadChange(Number(e.target.value))}
          disabled={sinStock}
          aria-label={`Cantidad de ${item.nombre}`}
          className={cn(
            'w-20 rounded-lg border border-slate-300 px-2 py-1.5 text-sm',
            'focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20',
            'disabled:cursor-not-allowed disabled:bg-slate-100 disabled:text-slate-400',
          )}
        />
      </td>

      <td
        className={cn(
          'px-4 py-3 text-sm font-semibold whitespace-nowrap',
          sinStock ? 'text-red-500' : 'text-slate-900',
        )}
      >
        {formatoMoneda(subtotal)}
      </td>

      <td className="px-4 py-3 text-right">
        <Button
          type="button"
          variant="secondary"
          onClick={onQuitar}
          className="px-2 py-1 text-xs"
          aria-label={`Quitar ${item.nombre} de la venta`}
        >
          Quitar
        </Button>
      </td>
    </tr>
  );
}
