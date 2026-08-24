import type { ValidarTicketResponse } from '@/types/api';
import { cn } from '@/utils/cn';
import { Button } from './Button';

interface CompraOriginalCardProps {
  /** Datos de la compra original devueltos por el backend (HU-04) */
  compra: ValidarTicketResponse;
  /** ID del ítem seleccionado para cambiar (controlado por el contenedor) */
  itemSeleccionadoId?: string | null;
  /** Callback al seleccionar un ítem de la compra */
  onSeleccionarItem?: (productoId: string) => void;
  /** Callback para retener el ticket e iniciar el cambio */
  onIniciarCambio?: () => void;
  /** True mientras se procesa la retención del ticket */
  retencionEnCurso?: boolean;
  /** True si el ticket ya quedó retenido como EN_CAMBIO */
  ticketRetenido?: boolean;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Tarjeta que muestra la compra original asociada a un ticket válido (HU-04).
 *
 * 📋 Información mostrada:
 * - Número de ticket y fecha de compra
 * - Cajero original
 * - Ítems comprados, con selección opcional del producto a cambiar
 * - Acción para retener el ticket e iniciar el cambio
 *
 * SRP: Solo presenta los datos y emite callbacks, sin lógica de negocio.
 */
export function CompraOriginalCard({
  compra,
  itemSeleccionadoId,
  onSeleccionarItem,
  onIniciarCambio,
  retencionEnCurso,
  ticketRetenido,
  className,
}: CompraOriginalCardProps) {
  const fecha = new Date(compra.fecha_compra);
  const total = compra.items.reduce(
    (acc, item) => acc + item.precio * item.cantidad,
    0,
  );
  const seleccionHabilitada = Boolean(onSeleccionarItem) && !ticketRetenido;

  return (
    <article
      className={cn(
        'overflow-hidden rounded-lg border-2 border-sky-200 bg-white shadow-md',
        className,
      )}
      aria-label="Compra original del ticket"
    >
      {/* Header */}
      <div className="border-b border-sky-100 bg-sky-50 px-6 py-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-xs font-medium uppercase tracking-wider text-sky-700">
              Compra Original
            </p>
            <p className="mt-1 font-mono text-lg font-bold text-sky-900">
              {compra.numero_ticket}
            </p>
          </div>
          {ticketRetenido && (
            <span className="rounded-full bg-sky-600 px-3 py-1 text-xs font-semibold uppercase text-white">
              EN_CAMBIO
            </span>
          )}
        </div>
        <p className="mt-1 text-xs text-sky-700">
          Comprado el{' '}
          <strong>
            {fecha.toLocaleDateString('es-AR')}{' '}
            {fecha.toLocaleTimeString('es-AR', {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </strong>{' '}
          · Cajero: <strong>{compra.cajero_original_id}</strong>
        </p>
      </div>

      {/* Ítems */}
      <div className="px-6 py-4">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-left text-xs uppercase text-slate-500">
              {seleccionHabilitada && (
                <th className="pb-2 pr-2" aria-label="Seleccionar producto" />
              )}
              <th className="pb-2">Producto</th>
              <th className="pb-2 text-center">Cant.</th>
              <th className="pb-2 text-right">Precio</th>
              <th className="pb-2 text-right">Subtotal</th>
            </tr>
          </thead>
          <tbody>
            {compra.items.map((item) => (
              <tr
                key={item.producto_id}
                className={cn(
                  'border-b border-slate-100 last:border-b-0',
                  seleccionHabilitada &&
                    itemSeleccionadoId === item.producto_id &&
                    'bg-sky-50',
                )}
              >
                {seleccionHabilitada && (
                  <td className="py-2 pr-2">
                    <input
                      type="radio"
                      name="producto-a-cambiar"
                      value={item.producto_id}
                      checked={itemSeleccionadoId === item.producto_id}
                      onChange={() => onSeleccionarItem?.(item.producto_id)}
                      aria-label={`Seleccionar ${item.nombre} para cambiar`}
                      className="h-4 w-4 cursor-pointer accent-brand-600"
                    />
                  </td>
                )}
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
        <div className="mt-4 border-t-2 border-slate-200 pt-3">
          <p className="flex items-center justify-between text-base font-bold text-slate-900">
            <span>TOTAL</span>
            <span>${total}</span>
          </p>
        </div>
      </div>

      {/* Acción */}
      {onIniciarCambio && !ticketRetenido && (
        <div className="border-t border-slate-200 bg-slate-50 px-6 py-4">
          <Button
            type="button"
            onClick={onIniciarCambio}
            disabled={!itemSeleccionadoId || retencionEnCurso}
            className="w-full"
          >
            {retencionEnCurso ? 'Reteniendo ticket...' : 'Iniciar cambio'}
          </Button>
          {!itemSeleccionadoId && (
            <p className="mt-2 text-center text-xs text-slate-500">
              Seleccioná el producto que querés cambiar.
            </p>
          )}
        </div>
      )}

      {/* Mensaje del backend */}
      <p className="border-t border-slate-200 px-6 py-3 text-xs text-slate-500">
        {compra.mensaje}
      </p>
    </article>
  );
}
