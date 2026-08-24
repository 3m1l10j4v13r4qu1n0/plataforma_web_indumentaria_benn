import type { EstadoProducto } from '@/types/api';
import { cn } from '@/utils/cn';
import { Button } from './Button';

export interface ValidarEstadoFormValues {
  estadoProducto: EstadoProducto | null;
  tieneEtiqueta: boolean;
  observaciones: string;
}

interface EstadoProductoSelectorProps {
  /** Valores actuales de la inspección física */
  value: ValidarEstadoFormValues;
  /** Callback cuando cambian los valores */
  onChange: (values: ValidarEstadoFormValues) => void;
  /** Callback al confirmar la validación del estado */
  onSubmit?: () => void;
  /** Estado de carga del envío al backend */
  isPending?: boolean;
  /** Si está deshabilitado (ej. cambio aún no registrado) */
  disabled?: boolean;
  /** Clase CSS adicional */
  className?: string;
}

const OPCIONES_ESTADO: Array<{
  valor: EstadoProducto;
  etiqueta: string;
  descripcion: string;
}> = [
  {
    valor: 'NUEVO_ETIQUETADO',
    etiqueta: 'Nuevo con etiqueta',
    descripcion: 'Sin uso y conserva su etiqueta original',
  },
  {
    valor: 'USADO',
    etiqueta: 'Usado',
    descripcion: 'Presenta señales de haber sido utilizado',
  },
  {
    valor: 'DANADO',
    etiqueta: 'Dañado',
    descripcion: 'Tiene roturas, manchas o defectos',
  }];

/**
 * Selector del estado físico del producto para su inspección (HU-03).
 *
 * 🎨 Validaciones visuales:
 * - Solo "Nuevo con etiqueta" es candidato válido al cambio
 * - El resumen indica en verde/rojo si la combinación elegida es apta
 * - La validación definitiva la realiza el backend
 *
 * SRP: Solo presenta el selector y emite cambios/callbacks.
 */
export function EstadoProductoSelector({
  value,
  onChange,
  onSubmit,
  isPending,
  disabled,
  className,
}: EstadoProductoSelectorProps) {
  const { estadoProducto, tieneEtiqueta, observaciones } = value;

  const esApto =
    estadoProducto === 'NUEVO_ETIQUETADO' && tieneEtiqueta;
  const seleccionCompleta = estadoProducto !== null;

  return (
    <section
      className={cn(
        'rounded-lg border border-slate-200 bg-white p-6 shadow-sm',
        className,
      )}
      aria-label="Validar estado físico del producto"
    >
      <h2 className="text-lg font-semibold text-slate-900">
        Validar estado del producto
      </h2>
      <p className="mt-1 text-sm text-slate-500">
        Inspeccioná el producto que trae el cliente.
      </p>

      {/* Selector de estado */}
      <fieldset className="mt-4" disabled={disabled || isPending}>
        <legend className="mb-2 text-sm font-medium text-slate-700">
          Estado físico *
        </legend>
        <div className="grid gap-2 sm:grid-cols-3">
          {OPCIONES_ESTADO.map((opcion) => (
            <label
              key={opcion.valor}
              className={cn(
                'cursor-pointer rounded-lg border p-3 text-sm transition-colors',
                'has-checked:border-brand-500 has-checked:bg-brand-50 has-checked:ring-1 has-checked:ring-brand-500/30',
                opcion.valor === 'NUEVO_ETIQUETADO'
                  ? 'hover:border-emerald-300'
                  : 'hover:border-rose-300',
                (disabled || isPending) && 'cursor-not-allowed opacity-60',
              )}
            >
              <input
                type="radio"
                name="estado-producto"
                value={opcion.valor}
                checked={estadoProducto === opcion.valor}
                onChange={() => onChange({ ...value, estadoProducto: opcion.valor })}
                className="sr-only"
                aria-label={opcion.etiqueta}
              />
              <span className="block font-medium text-slate-900">
                {opcion.etiqueta}
              </span>
              <span className="mt-0.5 block text-xs text-slate-500">
                {opcion.descripcion}
              </span>
            </label>
          ))}
        </div>
      </fieldset>

      {/* Etiqueta */}
      <label className="mt-4 flex items-center gap-2 text-sm text-slate-700">
        <input
          type="checkbox"
          checked={tieneEtiqueta}
          onChange={(e) =>
            onChange({ ...value, tieneEtiqueta: e.target.checked })
          }
          disabled={disabled || isPending}
          className="h-4 w-4 cursor-pointer accent-brand-600"
        />
        El producto conserva su etiqueta original
      </label>

      {/* Observaciones */}
      <label className="mt-4 block text-sm text-slate-700">
        <span className="mb-1 block">Observaciones</span>
        <textarea
          value={observaciones}
          onChange={(e) => onChange({ ...value, observaciones: e.target.value })}
          placeholder="Comentarios sobre la inspección (obligatorios si el producto no es apto)"
          rows={2}
          disabled={disabled || isPending}
          className="w-full resize-none rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
          aria-label="Observaciones de la inspección"
        />
      </label>

      {/* Resumen visual */}
      {seleccionCompleta && (
        <div
          className={cn(
            'mt-4 rounded-lg border px-3 py-2 text-sm',
            esApto
              ? 'border-emerald-200 bg-emerald-50 text-emerald-800'
              : 'border-rose-200 bg-rose-50 text-rose-800',
          )}
          role="status"
        >
          {esApto
            ? '✓ Producto candidato válido para el cambio.'
            : '✗ Producto no apto: solo se aceptan productos nuevos y con etiqueta.'}
        </div>
      )}

      {onSubmit && (
        <Button
          type="button"
          onClick={onSubmit}
          disabled={
            disabled ||
            isPending ||
            !seleccionCompleta ||
            (!esApto && observaciones.trim().length === 0)
          }
          className="mt-6 w-full"
        >
          {isPending ? 'Validando...' : 'Confirmar inspección'}
        </Button>
      )}
      {seleccionCompleta && !esApto && (
        <p className="mt-2 text-center text-xs text-slate-500">
          Las observaciones son obligatorias para registrar un rechazo.
        </p>
      )}
    </section>
  );
}
