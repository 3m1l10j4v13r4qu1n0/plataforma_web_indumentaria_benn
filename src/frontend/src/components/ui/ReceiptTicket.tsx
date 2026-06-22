import { cn } from '@/utils/cn';
import { formatCurrency } from '@/utils/formatCurrency';
import type { Ticket } from '@/types/domain';

interface ReceiptTicketProps {
  /** Datos completos del ticket */
  ticket: Ticket;
  /** Nombre del negocio (opcional, default: "SGVIR Retail") */
  nombreNegocio?: string;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Componente que renderiza un ticket con formato de papel térmico.
 *
 * 🎨 Diseño visual:
 * - Ancho fijo de 80mm (estándar de impresoras térmicas)
 * - Líneas punteadas para separar secciones
 * - Fuente monoespaciada para alineación
 * - Código de barras simulado (visual, no funcional)
 *
 * SRP: Solo presenta el ticket, sin lógica de impresión ni estado.
 */
export function ReceiptTicket({
  ticket,
  nombreNegocio = 'SGVIR Retail',
  className,
}: ReceiptTicketProps) {
  const fechaFormateada = new Date(ticket.fechaHora).toLocaleString('es-AR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <article
      className={cn(
        'mx-auto w-[320px] rounded-lg bg-white p-4 font-mono text-xs shadow-lg',
        'border border-slate-200',
        className,
      )}
      aria-label="Ticket de venta"
    >
      {/* Header del negocio */}
      <div className="mb-3 text-center">
        <h2 className="text-base font-bold uppercase tracking-wide">
          {nombreNegocio}
        </h2>
        <p className="mt-1 text-slate-600">Sistema de Gestión de Ventas</p>
      </div>

      {/* Línea punteada */}
      <div className="border-t-2 border-dashed border-slate-400" />

      {/* Información del ticket */}
      <div className="my-3 space-y-1">
        <div className="flex justify-between">
          <span className="text-slate-600">Ticket N°:</span>
          <span className="font-semibold">{ticket.numeroTicket}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-600">Fecha:</span>
          <span>{fechaFormateada}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-600">Cajero:</span>
          <span>{ticket.vendedorId}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-600">Estado:</span>
          <span className="font-semibold text-emerald-700">{ticket.estado}</span>
        </div>
      </div>

      {/* Línea punteada */}
      <div className="border-t-2 border-dashed border-slate-400" />

      {/* Tabla de items */}
      <div className="my-3">
        <div className="mb-2 flex justify-between border-b border-slate-300 pb-1 font-semibold">
          <span className="flex-1">ITEM</span>
          <span className="w-12 text-center">CANT</span>
          <span className="w-20 text-right">SUBTOTAL</span>
        </div>

        <div className="space-y-2">
          {ticket.items.map((item) => (
            <div key={item.productoId} className="flex justify-between">
              <div className="flex-1 pr-2">
                <div className="truncate font-medium">{item.nombre}</div>
                <div className="text-slate-500">
                  {formatCurrency(item.precioUnitario)} c/u
                </div>
              </div>
              <div className="w-12 text-center">{item.cantidad}</div>
              <div className="w-20 text-right font-semibold">
                {formatCurrency(item.subtotal)}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Línea punteada */}
      <div className="border-t-2 border-dashed border-slate-400" />

      {/* Totales */}
      <div className="my-3 space-y-1">
        <div className="flex justify-between text-slate-600">
          <span>Total artículos:</span>
          <span>{ticket.totalArticulos}</span>
        </div>
        <div className="flex justify-between border-t border-slate-300 pt-2 text-base font-bold">
          <span>TOTAL:</span>
          <span className="text-emerald-700">
            {formatCurrency(ticket.totalPagar)}
          </span>
        </div>
      </div>

      {/* Línea punteada */}
      <div className="border-t-2 border-dashed border-slate-400" />

      {/* Mensaje de agradecimiento */}
      <div className="my-3 text-center">
        <p className="font-semibold">¡Gracias por su compra!</p>
        <p className="mt-1 text-slate-500">Conserve este ticket para cambios</p>
      </div>

      {/* Línea punteada */}
      <div className="border-t-2 border-dashed border-slate-400" />

      {/* Código de barras simulado */}
      <div className="my-3 text-center">
        <div className="flex justify-center gap-[1px]">
          {Array.from({ length: 40 }).map((_, i) => (
            <div
              key={i}
              className={cn(
                'h-12',
                i % 3 === 0 ? 'w-[2px]' : 'w-[1px]',
                'bg-slate-900',
              )}
            />
          ))}
        </div>
        <p className="mt-1 font-mono text-[10px] tracking-wider">
          {ticket.numeroTicket}
        </p>
      </div>
    </article>
  );
}
