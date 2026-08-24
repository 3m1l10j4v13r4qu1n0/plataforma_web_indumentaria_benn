import type { VentaResponse } from '@/types/api';
import { cn } from '@/utils/cn';
import { Button } from './Button';
import { formatoFechaCorta, formatoMoneda } from '@/utils/format';

interface TicketCardProps {
  /** Datos de la venta confirmada (incluye ticket) */
  venta: VentaResponse;
  /** Callback para imprimir el ticket */
  onImprimir: () => void;
  /** Callback para cerrar el ticket y volver al formulario */
  onCerrar: () => void;
  /**
   * Muestra el toast "Advertencia de Impresión" (estado E-07 del contrato).
   * Se activará cuando exista integración real con la impresora; hoy el
   * navegador no expone detección de fallos de impresión.
   */
  advertenciaImpresion?: boolean;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Comprobante de venta generado (HU-07), según el contrato visual
 * (docs/05_mockups/mockup_hu07.html): card vertical centrada, header verde
 * de éxito, cuerpo monoespaciado con branding y acciones apiladas.
 *
 * SRP: Solo presenta datos del ticket, sin lógica de negocio.
 */
export function TicketCard({
  venta,
  onImprimir,
  onCerrar,
  advertenciaImpresion = false,
  className,
}: TicketCardProps) {
  return (
    <article
      className={cn(
        'overflow-hidden rounded-xl bg-white shadow-2xl',
        className,
      )}
      aria-label="Ticket de venta"
    >
      {/* Header de éxito */}
      <div className="bg-green-600 px-6 py-5 text-center text-white">
        <div className="mx-auto mb-2 flex h-12 w-12 items-center justify-center rounded-full bg-white/20">
          <svg
            className="h-7 w-7"
            fill="none"
            stroke="currentColor"
            strokeWidth={3}
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h2 className="text-lg font-bold">¡Venta Registrada!</h2>
        <p className="mt-1 text-sm text-green-100">
          La operación se guardó correctamente en el sistema.
        </p>
      </div>

      {/* Cuerpo del comprobante */}
      <div className="px-6 py-5 font-mono text-sm text-slate-800">
        <div className="border-b border-dashed border-slate-300 pb-3 text-center">
          <p className="font-bold">TIENDA RETAIL S.A.</p>
          <p className="text-xs text-slate-500">RUC: 20123456789</p>
          <p className="mt-1 text-xs text-slate-600">
            {formatoFechaCorta(venta.fecha_hora, { conSegundos: true })}
          </p>
        </div>

        {/* Ítems */}
        <ul className="py-2">
          {venta.items.map((item) => (
            <li
              key={item.producto_id}
              className="flex items-baseline justify-between gap-2 border-b border-dashed border-slate-200 py-2 last:border-b-0"
            >
              <span className="truncate">
                {item.cantidad}x {item.nombre}
              </span>
              <span>{formatoMoneda(item.precio * item.cantidad)}</span>
            </li>
          ))}
        </ul>

        {/* Total */}
        <div className="flex items-baseline justify-between border-t-2 border-dashed border-slate-300 pt-3 text-base font-bold">
          <span>TOTAL</span>
          <span>{formatoMoneda(venta.total ?? 0)}</span>
        </div>

        {/* Comprobante N° */}
        <div className="mt-3 text-center">
          <p className="text-xs uppercase tracking-wide text-slate-400">
            COMPROBANTE N°
          </p>
          <p className="font-semibold">{venta.numero_ticket}</p>
        </div>
      </div>

      {/* Acciones */}
      <div className="flex flex-col gap-2 px-6 pb-6">
        <Button type="button" onClick={onImprimir} className="w-full">
          Imprimir Comprobante
        </Button>
        <Button
          type="button"
          variant="secondary"
          onClick={onCerrar}
          className="w-full"
        >
          Nueva venta
        </Button>
      </div>

      {/* Toast de advertencia de impresión (E-07): la venta ya está registrada */}
      {advertenciaImpresion && (
        <div
          role="alert"
          className="fixed right-4 top-4 z-50 max-w-sm rounded-lg border-l-4 border-orange-500 bg-orange-50 p-4 shadow-lg"
        >
          <p className="text-sm font-bold text-orange-800">
            Advertencia de Impresión
          </p>
          <p className="mt-1 text-sm text-orange-700">
            La venta se registró, pero la impresora está desconectada. ¿Desea
            reintentar?
          </p>
          <button
            type="button"
            onClick={onImprimir}
            className="mt-2 text-sm font-medium text-orange-700 underline hover:text-orange-900"
          >
            Reintentar impresión
          </button>
        </div>
      )}
    </article>
  );
}
