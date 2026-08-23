import type { VentaResponse } from '@/types/api';
import { cn } from '@/utils/cn';
import { Button } from './Button';

interface TicketCardProps {
  /** Datos de la venta confirmada (incluye ticket) */
  venta: VentaResponse;
  /** Callback para imprimir el ticket */
  onImprimir: () => void;
  /** Callback para cerrar el ticket y volver al formulario */
  onCerrar: () => void;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Tarjeta que muestra el ticket de venta generado (HU-07).
 *
 * 📋 Información mostrada:
 * - Número de ticket
 * - Fecha y hora
 * - Items vendidos con nombre, cantidad y precio
 * - Total de la venta
 * - Botón imprimir y cerrar
 *
 * SRP: Solo presenta datos del ticket, sin lógica de negocio.
 */
export function TicketCard({
  venta,
  onImprimir,
  onCerrar,
  className,
}: TicketCardProps) {
  const fecha = new Date(venta.fecha_hora);

  return (
    <article
      className={cn(
        'rounded-lg border-2 border-emerald-200 bg-white shadow-md',
        className,
      )}
      aria-label="Ticket de venta"
    >
      {/* Header del ticket */}
      <div className="border-b border-emerald-100 bg-emerald-50 px-6 py-4 text-center">
        <p className="text-xs font-medium uppercase tracking-wider text-emerald-700">
          Comprobante de Venta
        </p>
        <p className="mt-1 font-mono text-lg font-bold text-emerald-900">
          {venta.numero_ticket}
        </p>
        <p className="text-xs text-emerald-600">
          {fecha.toLocaleDateString('es-AR')}{' '}
          {fecha.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>

      {/* Items */}
      <div className="px-6 py-4">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-left text-xs uppercase text-slate-500">
              <th className="pb-2">Producto</th>
              <th className="pb-2 text-center">Cant.</th>
              <th className="pb-2 text-right">Precio</th>
              <th className="pb-2 text-right">Subtotal</th>
            </tr>
          </thead>
          <tbody>
            {venta.items.map((item) => (
              <tr key={item.producto_id} className="border-b border-slate-100 last:border-b-0">
                <td className="py-2 font-medium text-slate-900">{item.nombre}</td>
                <td className="py-2 text-center text-slate-600">{item.cantidad}</td>
                <td className="py-2 text-right text-slate-600">${item.precio}</td>
                <td className="py-2 text-right font-semibold text-slate-900">
                  ${item.precio * item.cantidad}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Total */}
        <div className="mt-4 border-t-2 border-emerald-200 pt-3">
          <p className="flex items-center justify-between text-base font-bold text-slate-900">
            <span>TOTAL</span>
            <span>${venta.total}</span>
          </p>
        </div>
      </div>

      {/* Footer del ticket */}
      <div className="border-t border-slate-200 bg-slate-50 px-6 py-3 text-center">
        <p className="text-xs text-slate-500">
          Vendedor: {venta.vendedor_id} | Venta: {venta.id}
        </p>
      </div>

      {/* Acciones */}
      <div className="flex gap-3 border-t border-slate-200 px-6 py-4">
        <Button
          type="button"
          variant="secondary"
          onClick={onCerrar}
          className="flex-1"
        >
          Nueva venta
        </Button>
        <Button
          type="button"
          onClick={onImprimir}
          className="flex-1"
        >
          Imprimir ticket
        </Button>
      </div>
    </article>
  );
}
