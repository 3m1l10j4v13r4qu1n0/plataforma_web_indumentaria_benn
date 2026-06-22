import { cn } from '@/utils/cn';
import { formatCurrency } from '@/utils/formatCurrency';
import { StockIndicator } from './StockIndicator';
import { QuantityInput } from './QuantityInput';

export interface CartItemRowProps {
  /** Nombre del producto */
  nombre: string;
  /** SKU/código del producto */
  codigo: string;
  /** Precio unitario */
  precio: number;
  /** Stock disponible */
  stockActual: number;
  /** Cantidad a vender */
  cantidad: number;
  /** Callback cuando cambia la cantidad */
  onQuantityChange: (cantidad: number) => void;
  /** Callback para eliminar el item */
  onRemove: () => void;
  /** Si el item tiene error de stock (cantidad > stock) */
  hasStockError?: boolean;
  /** Si está deshabilitado */
  disabled?: boolean;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Fila de la tabla que muestra un producto en el carrito de venta.
 *
 * 📋 Información mostrada (alineada con mockup HU-01):
 * - Nombre + SKU
 * - Precio unitario
 * - Stock disponible (con indicador visual)
 * - Input de cantidad (con controles +/−)
 * - Subtotal (precio × cantidad)
 * - Botón eliminar
 *
 * SRP: Solo presenta datos, sin lógica de negocio.
 */
export function CartItemRow({
  nombre,
  codigo,
  precio,
  stockActual,
  cantidad,
  onQuantityChange,
  onRemove,
  hasStockError = false,
  disabled = false,
  className,
}: CartItemRowProps) {
  const subtotal = precio * cantidad;
  const isOutOfStock = stockActual === 0;

  return (
    <tr
      className={cn(
        'border-b border-slate-200 transition-colors',
        hasStockError && 'bg-rose-50',
        !hasStockError && 'hover:bg-slate-50',
        className,
      )}
      aria-invalid={hasStockError}
    >
      {/* Producto (nombre + SKU) */}
      <td className="px-4 py-3">
        <div className="flex flex-col">
          <span className="text-sm font-medium text-slate-900">{nombre}</span>
          <span className="text-xs text-slate-500">SKU: {codigo}</span>
        </div>
      </td>

      {/* Precio unitario */}
      <td className="px-4 py-3 text-right">
        <span className="text-sm font-medium text-slate-700">
          {formatCurrency(precio)}
        </span>
      </td>

      {/* Stock actual */}
      <td className="px-4 py-3 text-center">
        <StockIndicator quantity={stockActual} />
      </td>

      {/* Cantidad (input con controles) */}
      <td className="px-4 py-3 text-center">
        <QuantityInput
          value={cantidad}
          onChange={onQuantityChange}
          max={stockActual}
          disabled={disabled || isOutOfStock}
          hasError={hasStockError}
        />
      </td>

      {/* Subtotal */}
      <td className="px-4 py-3 text-right">
        <span
          className={cn(
            'text-sm font-semibold',
            hasStockError ? 'text-rose-600' : 'text-slate-900',
          )}
        >
          {formatCurrency(subtotal)}
        </span>
      </td>

      {/* Acciones (eliminar) */}
      <td className="px-4 py-3 text-center">
        <button
          type="button"
          onClick={onRemove}
          disabled={disabled}
          className={cn(
            'inline-flex h-7 w-7 items-center justify-center rounded-md',
            'text-slate-400 transition-colors',
            'hover:bg-rose-50 hover:text-rose-600',
            'disabled:cursor-not-allowed disabled:opacity-50',
          )}
          aria-label={`Eliminar ${nombre} del carrito`}
        >
          <svg
            className="h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M1 7h22M9 7V4a1 1 0 011-1h4a1 1 0 011 1v3"
            />
          </svg>
        </button>
      </td>
    </tr>
  );
}
