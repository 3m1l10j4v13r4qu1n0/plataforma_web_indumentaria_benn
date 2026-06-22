import { cn } from '@/utils/cn';

interface SaleActionBarProps {
  /** Callback al cancelar la venta */
  onCancel: () => void;
  /** Callback al confirmar la venta */
  onConfirm: () => void;
  /** Si el botón de confirmar está deshabilitado */
  confirmDisabled?: boolean;
  /** Si está procesando la venta (loading) */
  isProcessing?: boolean;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Barra de acciones de la venta con botones Cancelar y Confirmar.
 *
 * 🎯 Alineada con el mockup HU-01:
 * - Botón "Cancelar" (siempre habilitado)
 * - Botón "Confirmar Venta" (bloqueado si hay errores de stock)
 *
 * SRP: Solo presenta las acciones, sin lógica de negocio.
 */
export function SaleActionBar({
  onCancel,
  onConfirm,
  confirmDisabled = false,
  isProcessing = false,
  className,
}: SaleActionBarProps) {
  const confirmLabel = isProcessing ? 'Procesando...' : 'Confirmar Venta';

  return (
    <div
      className={cn(
        'flex items-center justify-end gap-3 rounded-lg border border-slate-200 bg-white p-4 shadow-sm',
        className,
      )}
    >
      <button
        type="button"
        onClick={onCancel}
        disabled={isProcessing}
        className={cn(
          'rounded-lg border border-slate-300 bg-white px-5 py-2.5 text-sm font-medium text-slate-700',
          'transition-colors hover:bg-slate-50',
          'focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2',
          'disabled:cursor-not-allowed disabled:opacity-50',
        )}
      >
        Cancelar
      </button>

      <button
        type="button"
        onClick={onConfirm}
        disabled={confirmDisabled || isProcessing}
        className={cn(
          'rounded-lg px-5 py-2.5 text-sm font-medium text-white transition-colors',
          'focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2',
          'disabled:cursor-not-allowed',
          confirmDisabled || isProcessing
            ? 'bg-slate-400'
            : 'bg-brand-600 hover:bg-brand-700',
        )}
        aria-disabled={confirmDisabled}
      >
        {isProcessing && (
          <span
            className="mr-2 inline-block h-3 w-3 animate-spin rounded-full border-2 border-white border-t-transparent"
            aria-hidden="true"
          />
        )}
        {confirmLabel}
        {confirmDisabled && !isProcessing && (
          <span className="ml-1 text-xs">(Bloqueado)</span>
        )}
      </button>
    </div>
  );
}
