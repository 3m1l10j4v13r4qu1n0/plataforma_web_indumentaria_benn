import { useState } from 'react';
import type { ItemTicketResponse } from '@/types/api';
import { Button } from './Button';
import { cn } from '@/utils/cn';

export interface RegistroCambioFormValues {
  cajeroId: string;
  nuevoProductoId: string;
  motivo: string;
}

interface RegistroCambioFormProps {
  /** Producto seleccionado de la compra original que se va a cambiar */
  productoACambiar: ItemTicketResponse | null;
  /** Callback al confirmar el registro del cambio (HU-02) */
  onSubmit: (values: RegistroCambioFormValues) => void;
  /** Estado de carga del envío al backend */
  isPending?: boolean;
  /** Si está deshabilitado (ej. ticket no retenido aún) */
  disabled?: boolean;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Formulario para registrar el cambio de un producto (HU-02).
 *
 * El backend valida el plazo de 15 días; este formulario solo
 * recolecta los datos y hace validaciones básicas de completitud.
 *
 * SRP: Solo presenta el formulario; la llamada al backend queda en el hook.
 */
export function RegistroCambioForm({
  productoACambiar,
  onSubmit,
  isPending,
  disabled,
  className,
}: RegistroCambioFormProps) {
  const [cajeroId, setCajeroId] = useState('');
  const [nuevoProductoId, setNuevoProductoId] = useState('');
  const [motivo, setMotivo] = useState('');

  const formularioValido =
    cajeroId.trim().length > 0 &&
    nuevoProductoId.trim().length > 0 &&
    productoACambiar !== null;

  const handleSubmit = () => {
    if (!formularioValido || !productoACambiar) return;
    onSubmit({
      cajeroId: cajeroId.trim(),
      nuevoProductoId: nuevoProductoId.trim(),
      motivo: motivo.trim(),
    });
  };

  return (
    <section
      className={cn(
        'rounded-lg border border-slate-200 bg-white p-6 shadow-sm',
        className,
      )}
      aria-label="Registrar cambio de producto"
    >
      <h2 className="text-lg font-semibold text-slate-900">
        Registrar cambio
      </h2>

      {/* Producto a cambiar (viene de la selección en la compra original) */}
      <div className="mt-4 rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm">
        <p className="text-xs uppercase tracking-wide text-slate-500">
          Producto a cambiar
        </p>
        {productoACambiar ? (
          <p className="mt-1 font-medium text-slate-900">
            {productoACambiar.nombre}{' '}
            <span className="font-mono text-xs text-slate-500">
              ({productoACambiar.producto_id})
            </span>
          </p>
        ) : (
          <p className="mt-1 text-slate-400">Sin producto seleccionado.</p>
        )}
      </div>

      <div className="mt-4 space-y-4">
        {/* Cajero */}
        <label className="block text-sm text-slate-700">
          <span className="mb-1 block">ID del cajero *</span>
          <input
            type="text"
            value={cajeroId}
            onChange={(e) => setCajeroId(e.target.value)}
            placeholder="Ej: C-005"
            disabled={disabled || isPending}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            aria-label="ID del cajero que procesa el cambio"
          />
        </label>

        {/* Nuevo producto */}
        <label className="block text-sm text-slate-700">
          <span className="mb-1 block">ID del nuevo producto *</span>
          <input
            type="text"
            value={nuevoProductoId}
            onChange={(e) => setNuevoProductoId(e.target.value)}
            placeholder="Ej: 124"
            disabled={disabled || isPending}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            aria-label="ID del nuevo producto de reemplazo"
          />
        </label>

        {/* Motivo */}
        <label className="block text-sm text-slate-700">
          <span className="mb-1 block">Motivo del cambio</span>
          <textarea
            value={motivo}
            onChange={(e) => setMotivo(e.target.value)}
            placeholder="Ej: Talla incorrecta"
            rows={2}
            disabled={disabled || isPending}
            className="w-full resize-none rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            aria-label="Motivo del cambio"
          />
        </label>
      </div>

      <Button
        type="button"
        onClick={handleSubmit}
        disabled={disabled || isPending || !formularioValido}
        className="mt-6 w-full"
      >
        {isPending ? 'Registrando cambio...' : 'Registrar cambio'}
      </Button>
      <p className="mt-2 text-center text-xs text-slate-500">
        El sistema valida automáticamente el plazo de 15 días desde la compra.
      </p>
    </section>
  );
}
