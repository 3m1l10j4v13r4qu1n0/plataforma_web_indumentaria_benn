import { cn } from '@/utils/cn';
import { StockBadge, type StockLevel } from './StockBadge';
import { Button } from './Button';
import type { StockProducto } from '@/types/domain';

export interface VentaProductoCardProps {
  /** Producto consultado con su stock disponible */
  producto: StockProducto;
  /** Cantidad seleccionada a vender */
  cantidad: number;
  /** Callback cuando cambia la cantidad */
  onCantidadChange: (cantidad: number) => void;
  /** Callback para agregar el producto a la venta */
  onAgregar: () => void;
  /** Si ya fue agregado al carrito (deshabilita) */
  yaAgregado?: boolean;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Tarjeta de producto para el flujo de venta (HU-01).
 *
 * Muestra el stock disponible, la cantidad a vender y permite
 * agregar el producto a la venta. El botón se deshabilita si
 * el stock es cero (la decisión de negocio la toma el contenedor).
 *
 * SRP: Solo presenta datos y emite callbacks, sin lógica de negocio.
 */
export function VentaProductoCard({
  producto,
  cantidad,
  onCantidadChange,
  onAgregar,
  yaAgregado = false,
  className,
}: VentaProductoCardProps) {
  const sinStock = producto.stockActual === 0;
  const stockLevel: StockLevel = sinStock ? 'out' : 'healthy';

  return (
    <article
      className={cn(
        'rounded-lg border border-slate-200 bg-white p-4 shadow-sm',
        className,
      )}
    >
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex-1">
          <h3 className="text-base font-semibold text-slate-900">
            {producto.nombre}
          </h3>
          <p className="mt-1 text-sm text-slate-600">
            Código: <span className="font-mono font-medium">{producto.productoId}</span>
            <span className="mx-2 text-slate-400">|</span>
            Categoría: <span className="font-medium">{producto.categoria}</span>
          </p>
          <p className="mt-1 text-sm text-slate-600">
            Precio: <span className="font-medium">${producto.precio}</span>
          </p>
        </div>

        <div className="flex items-center">
          <StockBadge level={stockLevel} quantity={producto.stockActual} />
        </div>
      </div>

      <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <label className="flex items-center gap-2 text-sm text-slate-700">
          <span>Cantidad:</span>
          <input
            type="number"
            min={1}
            max={producto.stockActual}
            value={cantidad}
            onChange={(e) => onCantidadChange(Number(e.target.value))}
            disabled={sinStock}
            className={cn(
              'w-24 rounded-lg border border-slate-300 px-3 py-1.5 text-sm',
              'focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20',
              'disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-500',
            )}
            aria-label="Cantidad a vender"
          />
        </label>

        <Button
          type="button"
          onClick={onAgregar}
          disabled={sinStock || yaAgregado || cantidad < 1}
        >
          {sinStock ? 'Sin stock' : yaAgregado ? 'Agregado' : 'Agregar a venta'}
        </Button>
      </div>
    </article>
  );
}