import { cn } from '@/utils/cn';
import { Button } from './Button';

export interface VentaItem {
  productoId: string;
  nombre: string;
  precio: number;
  cantidad: number;
}

interface VentaItemRowProps {
  /** Item del resumen de venta */
  item: VentaItem;
  /** Callback para quitar el item de la venta */
  onQuitar: () => void;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Fila de un item en el resumen de la venta (HU-01).
 *
 * Muestra nombre, cantidad, subtotal y un botón para quitarlo.
 *
 * SRP: Solo presenta el item y emite callbacks, sin lógica de negocio.
 */
export function VentaItemRow({ item, onQuitar, className }: VentaItemRowProps) {
  const subtotal = item.precio * item.cantidad;

  return (
    <li
      className={cn(
        'flex items-center justify-between gap-3 border-b border-slate-100 py-2 last:border-b-0',
        className,
      )}
    >
      <div className="min-w-0 flex-1">
        <p className="truncate text-sm font-medium text-slate-900">{item.nombre}</p>
        <p className="text-xs text-slate-500">
          {item.cantidad} × ${item.precio}
        </p>
      </div>

      <span className="text-sm font-semibold text-slate-900">${subtotal}</span>

      <Button
        type="button"
        variant="secondary"
        onClick={onQuitar}
        className="px-2 py-1 text-xs"
        aria-label={`Quitar ${item.nombre} de la venta`}
      >
        Quitar
      </Button>
    </li>
  );
}