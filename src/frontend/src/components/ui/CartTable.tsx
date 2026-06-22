import { cn } from '@/utils/cn';
import { CartItemRow, type CartItemRowProps } from './CartItemRow';
import { EmptyState } from './EmptyState';

interface CartTableProps {
  /** Lista de productos en el carrito */
  items: CartItemRowProps[];
  /** Si la tabla está deshabilitada (ej: mientras procesa venta) */
  disabled?: boolean;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Tabla contenedora del carrito de productos.
 *
 * SRP: Solo renderiza la estructura de la tabla y delega
 *      cada fila al componente CartItemRow.
 */
export function CartTable({ items, disabled, className }: CartTableProps) {
  if (items.length === 0) {
    return (
      <EmptyState
        title="Carrito vacío"
        description="Busca o escanea un producto para agregarlo a la venta."
        className="py-8"
      />
    );
  }

  return (
    <div
      className={cn('overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm', className)}
    >
      <div className="overflow-x-auto">
        <table className="w-full text-left" aria-label="Productos en el carrito">
          <thead className="bg-slate-50 text-xs uppercase tracking-wider text-slate-600">
            <tr>
              <th scope="col" className="px-4 py-3 font-semibold">
                Producto
              </th>
              <th scope="col" className="px-4 py-3 text-right font-semibold">
                Precio Unit.
              </th>
              <th scope="col" className="px-4 py-3 text-center font-semibold">
                Stock Actual
              </th>
              <th scope="col" className="px-4 py-3 text-center font-semibold">
                Cantidad
              </th>
              <th scope="col" className="px-4 py-3 text-right font-semibold">
                Subtotal
              </th>
              <th scope="col" className="px-4 py-3 text-center font-semibold">
                <span className="sr-only">Acciones</span>
              </th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <CartItemRow
                key={item.codigo}
                {...item}
                disabled={disabled}
              />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
