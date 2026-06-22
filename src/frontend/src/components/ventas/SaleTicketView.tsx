import { useCallback, useMemo } from 'react';
import { cn } from '@/utils/cn';
import {
  ReceiptTicket,
  PrinterStatusIndicator,
  PrintErrorModal,
} from '@/components/ui';
import { usePrinter } from '@/hooks/usePrinter';
import { toTicket } from '@/types/api';
import type { ItemCarrito, VentaProcesada } from '@/types/domain';

interface SaleTicketViewProps {
  /** Carrito con los items vendidos (antes de limpiarlo) */
  carrito: ItemCarrito[];
  /** Datos de la venta procesada por el backend */
  ventaProcesada: VentaProcesada;
  /** Total de artículos vendidos */
  totalArticulos: number;
  /** Total a pagar */
  totalPagar: number;
  /** Callback para iniciar una nueva venta (limpia todo) */
  onNuevaVenta: () => void;
}

/**
 * Vista post-venta que muestra el ticket impreso y simula la impresión.
 *
 * 🎯 Flujo (SRP):
 * 1. Muestra el ticket con formato de papel térmico
 * 2. Permite simular la impresión (botón "Imprimir")
 * 3. Si hay error, muestra modal con opciones (Reintentar/Omitir)
 * 4. Al finalizar, permite iniciar nueva venta
 *
 * ⚠️ YAGNI: La impresión es simulada (1.5s de delay). No se conecta
 * a impresora física ni usa window.print().
 */
export function SaleTicketView({
  carrito,
  ventaProcesada,
  totalArticulos,
  totalPagar,
  onNuevaVenta,
}: SaleTicketViewProps) {
  const { estado, print, retry, skip, reset } = usePrinter();

  // Construye el ticket una sola vez (memoizado)
  const ticket = useMemo(
    () =>
      toTicket({
        carrito,
        numeroTicket: ventaProcesada.numeroTicket,
        fechaHora: ventaProcesada.fechaHora,
        vendedorId: ventaProcesada.vendedorId,
        estado: ventaProcesada.estado,
        totalArticulos,
        totalPagar,
      }),
    [carrito, ventaProcesada, totalArticulos, totalPagar],
  );

  const handleRetry = useCallback(() => {
    retry();
  }, [retry]);

  const handleSkip = useCallback(() => {
    skip();
    onNuevaVenta();
  }, [skip, onNuevaVenta]);

  const handleCancelError = useCallback(() => {
    reset();
  }, [reset]);

  const handleNuevaVenta = useCallback(() => {
    reset();
    onNuevaVenta();
  }, [reset, onNuevaVenta]);

  return (
    <>
      <div className="space-y-6">
        {/* Header con estado de impresora */}
        <div className="flex flex-col items-center gap-4 sm:flex-row sm:justify-between">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              Venta Procesada Correctamente
            </h2>
            <p className="text-sm text-slate-600">
              Ticket N° <span className="font-mono font-semibold">{ticket.numeroTicket}</span>
            </p>
          </div>
          <PrinterStatusIndicator estado={estado} />
        </div>

        {/* Ticket visual */}
        <div className="flex justify-center">
          <ReceiptTicket ticket={ticket} />
        </div>

        {/* Acciones */}
        <div className="flex flex-col gap-3 sm:flex-row sm:justify-center">
          {estado === 'idle' && (
            <button
              type="button"
              onClick={print}
              className={cn(
                'rounded-lg bg-brand-600 px-6 py-2.5 text-sm font-medium text-white',
                'transition-colors hover:bg-brand-700',
                'focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2',
              )}
            >
              🖨️ Imprimir Ticket
            </button>
          )}

          {estado === 'success' && (
            <button
              type="button"
              onClick={handleNuevaVenta}
              autoFocus
              className={cn(
                'rounded-lg bg-emerald-600 px-6 py-2.5 text-sm font-medium text-white',
                'transition-colors hover:bg-emerald-700',
                'focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2',
              )}
            >
              ✓ Nueva Venta
            </button>
          )}

          {estado === 'printing' && (
            <div className="flex items-center gap-2 text-sm text-slate-600">
              <div className="h-4 w-4 animate-spin rounded-full border-2 border-brand-500 border-t-transparent" />
              Imprimiendo ticket...
            </div>
          )}

          {/* Botón de omitir siempre disponible (excepto durante printing) */}
          {estado !== 'printing' && (
            <button
              type="button"
              onClick={handleSkip}
              className={cn(
                'rounded-lg border border-slate-300 bg-white px-6 py-2.5 text-sm font-medium text-slate-700',
                'transition-colors hover:bg-slate-50',
                'focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2',
              )}
            >
              Omitir Impresión
            </button>
          )}
        </div>
      </div>

      {/* Modal de error de impresora */}
      <PrintErrorModal
        isOpen={estado === 'error'}
        onRetry={handleRetry}
        onSkip={handleSkip}
        onCancel={handleCancelError}
      />
    </>
  );
}
