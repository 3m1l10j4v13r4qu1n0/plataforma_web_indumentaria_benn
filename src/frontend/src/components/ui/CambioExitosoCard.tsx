import type { CambioResponse } from '@/types/api';
import { cn } from '@/utils/cn';
import { Button } from './Button';

interface CambioExitosoCardProps {
  /** Datos del cambio registrado devueltos por el backend (HU-02) */
  cambio: CambioResponse;
  /** Callback para iniciar otro cambio */
  onNuevoCambio: () => void;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Tarjeta de confirmación de un cambio registrado exitosamente (HU-02).
 *
 * 📋 Información mostrada:
 * - ID del cambio y estado
 * - Fecha del cambio y productos involucrados
 * - Motivo (si fue ingresado)
 * - Acción para registrar otro cambio
 *
 * SRP: Solo presenta los datos del cambio, sin lógica de negocio.
 */
export function CambioExitosoCard({
  cambio,
  onNuevoCambio,
  className,
}: CambioExitosoCardProps) {
  const fecha = new Date(cambio.fecha_cambio);

  return (
    <article
      className={cn(
        'rounded-lg border-2 border-emerald-200 bg-white shadow-md',
        className,
      )}
      aria-label="Cambio registrado"
    >
      {/* Header */}
      <div className="border-b border-emerald-100 bg-emerald-50 px-6 py-4 text-center">
        <p className="text-xs font-medium uppercase tracking-wider text-emerald-700">
          Cambio Registrado
        </p>
        <p className="mt-1 font-mono text-lg font-bold text-emerald-900">
          {cambio.id}
        </p>
        <p className="text-xs text-emerald-600">
          {fecha.toLocaleDateString('es-AR')}{' '}
          {fecha.toLocaleTimeString('es-AR', {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </p>
      </div>

      {/* Detalle */}
      <div className="space-y-2 px-6 py-4 text-sm">
        <p className="flex justify-between gap-3">
          <span className="text-slate-500">Venta original</span>
          <span className="font-mono font-medium text-slate-900">
            {cambio.venta_original_id}
          </span>
        </p>
        <p className="flex justify-between gap-3">
          <span className="text-slate-500">Producto cambiado</span>
          <span className="font-mono font-medium text-slate-900">
            {cambio.producto_a_cambiar_id}
          </span>
        </p>
        <p className="flex justify-between gap-3">
          <span className="text-slate-500">Nuevo producto</span>
          <span className="font-mono font-medium text-slate-900">
            {cambio.nuevo_producto_id}
          </span>
        </p>
        <p className="flex justify-between gap-3">
          <span className="text-slate-500">Estado</span>
          <span className="font-semibold uppercase text-emerald-700">
            {cambio.estado}
          </span>
        </p>
        {cambio.motivo && (
          <p className="border-t border-slate-100 pt-2 text-slate-600">
            Motivo: <em>{cambio.motivo}</em>
          </p>
        )}
      </div>

      {/* Acción */}
      <div className="border-t border-slate-200 bg-slate-50 px-6 py-4">
        <Button type="button" onClick={onNuevoCambio} className="w-full">
          Registrar otro cambio
        </Button>
      </div>
    </article>
  );
}
