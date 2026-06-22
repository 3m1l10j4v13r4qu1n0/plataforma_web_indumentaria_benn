import { useEffect } from 'react';
import { cn } from '@/utils/cn';
import { formatCurrency } from '@/utils/formatCurrency';

interface SaleSuccessModalProps {
  /** Número de ticket generado */
  numeroTicket: string;
  /** Total de la venta */
  totalPagar: number;
  /** Cantidad total de artículos vendidos */
  totalArticulos: number;
  /** Callback al cerrar el modal */
  onClose: () => void;
  /** Si el modal está visible */
  isOpen: boolean;
}

/**
 * Modal de confirmación de venta exitosa.
 *
 * 🎯 Alineado con el caso de uso expandido HU-01:
 * "El sistema procesa la venta, muestra un mensaje de 'Venta Exitosa'
 *  y limpia la pantalla para la siguiente operación."
 *
 * SRP: Solo presenta la confirmación, sin lógica de negocio.
 */
export function SaleSuccessModal({
  numeroTicket,
  totalPagar,
  totalArticulos,
  onClose,
  isOpen,
}: SaleSuccessModalProps) {
  // Cierra automáticamente después de 4 segundos (KISS)
  useEffect(() => {
    if (!isOpen) return;
    const timer = setTimeout(onClose, 4000);
    return () => clearTimeout(timer);
  }, [isOpen, onClose]);

  // Cierre con tecla Escape (accesibilidad)
  useEffect(() => {
    if (!isOpen) return;
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="sale-success-title"
    >
      <div
        className={cn(
          'w-full max-w-md rounded-xl bg-white p-6 shadow-2xl',
          'animate-in fade-in zoom-in-95 duration-200',
        )}
      >
        {/* Icono de éxito */}
        <div className="mb-4 flex justify-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-emerald-100">
            <svg
              className="h-8 w-8 text-emerald-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2.5}
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
        </div>

        {/* Contenido */}
        <div className="text-center">
          <h2
            id="sale-success-title"
            className="text-xl font-bold text-slate-900"
          >
            ¡Venta Exitosa!
          </h2>
          <p className="mt-2 text-sm text-slate-600">
            La venta ha sido procesada correctamente.
          </p>

          {/* Detalles de la venta */}
          <dl className="mt-4 space-y-2 rounded-lg bg-slate-50 p-4 text-left">
            <div className="flex justify-between">
              <dt className="text-sm text-slate-600">Ticket N°</dt>
              <dd className="font-mono text-sm font-semibold text-slate-900">
                {numeroTicket}
              </dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-sm text-slate-600">Artículos</dt>
              <dd className="text-sm font-semibold text-slate-900">
                {totalArticulos}
              </dd>
            </div>
            <div className="flex justify-between border-t border-slate-200 pt-2">
              <dt className="text-sm font-semibold text-slate-700">Total</dt>
              <dd className="text-lg font-bold text-brand-700">
                {formatCurrency(totalPagar)}
              </dd>
            </div>
          </dl>

          {/* Botón de cierre */}
          <button
            type="button"
            onClick={onClose}
            autoFocus
            className={cn(
              'mt-4 w-full rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-medium text-white',
              'transition-colors hover:bg-brand-700',
              'focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2',
            )}
          >
            Nueva Venta
          </button>
        </div>
      </div>
    </div>
  );
}
