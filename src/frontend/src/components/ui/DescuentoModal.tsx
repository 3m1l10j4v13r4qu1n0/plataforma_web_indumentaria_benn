import { useState } from 'react';
import { Button } from './Button';
import { Alert } from './Alert';
import { cn } from '@/utils/cn';
import { formatoMoneda } from '@/utils/format';

const LIMITE_SIN_AUTORIZACION = 20;

interface DescuentoModalProps {
  /** Si el modal está abierto */
  isOpen: boolean;
  /** Callback al cerrar el modal */
  onClose: () => void;
  /** Callback al confirmar el descuento */
  onConfirm: (datos: {
    porcentaje: number;
    motivo: string;
    autorizado_por: string | null;
  }) => void;
  /** Total de la venta para previsualizar el monto */
  totalVenta: number;
  /** Estado de carga del envío */
  isPending: boolean;
  /** Mensaje de error del backend (ej. credenciales inválidas, E-05) */
  error?: string | null;
}

/**
 * Modal para aplicar descuentos a una venta (HU-05).
 *
 * Sigue la estética del contrato visual (docs/05_mockups/mockup_hu05.html):
 * header naranja "Autorización Requerida", hint del límite y acción oscura
 * "Aplicar". El flujo es post-venta vía POST /descuentos (decisión D-002).
 *
 * SRP: Solo presenta el formulario de descuento; la lógica de
 * llamada al backend queda en el contenedor (CrearVentaPage).
 */
export function DescuentoModal({
  isOpen,
  onClose,
  onConfirm,
  totalVenta,
  isPending,
  error,
}: DescuentoModalProps) {
  const [porcentaje, setPorcentaje] = useState('');
  const [motivo, setMotivo] = useState('');
  const [autorizadoPor, setAutorizadoPor] = useState('');

  const porcentajeNum = parseFloat(porcentaje) || 0;
  const superaLimite = porcentajeNum > LIMITE_SIN_AUTORIZACION;
  const montoDescuento = (totalVenta * porcentajeNum) / 100;
  const totalConDescuento = totalVenta - montoDescuento;

  const formularioValido =
    porcentajeNum > 0 &&
    porcentajeNum <= 100 &&
    motivo.trim().length >= 5 &&
    (!superaLimite || autorizadoPor.trim().length > 0);

  const handleConfirm = () => {
    if (!formularioValido) return;
    onConfirm({
      porcentaje: porcentajeNum,
      motivo: motivo.trim(),
      autorizado_por: superaLimite ? autorizadoPor.trim() : null,
    });
  };

  const handleReset = () => {
    setPorcentaje('');
    setMotivo('');
    setAutorizadoPor('');
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={handleReset}
        aria-hidden="true"
      />

      {/* Modal */}
      <div
        role="dialog"
        aria-modal="true"
        aria-label={
          superaLimite ? 'Autorización Requerida' : 'Aplicar descuento'
        }
        className="relative mx-4 w-full max-w-md overflow-hidden rounded-xl border border-slate-200 bg-white shadow-2xl"
      >
        {/* Header */}
        {superaLimite ? (
          <div className="flex items-start gap-3 bg-orange-500 px-6 py-4 text-white">
            <svg
              className="mt-0.5 h-5 w-5 shrink-0"
              fill="none"
              stroke="currentColor"
              strokeWidth={2}
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
            <div>
              <h2 className="text-base font-bold">Autorización Requerida</h2>
              <p className="mt-0.5 text-sm text-orange-50">
                El descuento del {porcentajeNum}% supera el límite permitido ({LIMITE_SIN_AUTORIZACION}%).
              </p>
            </div>
          </div>
        ) : (
          <div className="px-6 pt-6">
            <h2 className="text-lg font-semibold text-slate-900">
              Aplicar descuento
            </h2>
            <p className="mt-1 text-sm text-slate-500">
              Total de la venta:{' '}
              <span className="font-medium">{formatoMoneda(totalVenta)}</span>
            </p>
          </div>
        )}

        <div className="space-y-4 px-6 py-5">
          {superaLimite && (
            <p className="text-sm text-slate-600">
              Para aplicar este descuento, un usuario con rol de{' '}
              <strong>Gerente</strong> debe autorizarlo. Esta acción quedará
              registrada en el sistema.
            </p>
          )}

          {/* Porcentaje con hint contractual del límite */}
          <label className="block text-sm text-slate-700">
            <span className="mb-1 block font-medium">
              Descuento (%){' '}
              <span className="font-normal text-slate-400">
                (Máx. {LIMITE_SIN_AUTORIZACION}% sin autorización)
              </span>
            </span>
            <div className="relative">
              <input
                type="number"
                min="0"
                max="100"
                step="0.01"
                value={porcentaje}
                onChange={(e) => setPorcentaje(e.target.value)}
                placeholder="Ej: 15"
                className={cn(
                  'w-full rounded-lg border px-3 py-1.5 pr-8 text-sm focus:outline-none focus:ring-2',
                  superaLimite
                    ? 'border-orange-300 bg-orange-50 text-orange-700 focus:border-orange-500 focus:ring-orange-500/20'
                    : 'border-slate-300 focus:border-brand-500 focus:ring-brand-500/20',
                )}
                disabled={isPending}
              />
              <span className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-slate-400">
                %
              </span>
            </div>
          </label>

          {/* Campo de autorización (condicional) */}
          {superaLimite && (
            <label className="block text-sm text-slate-700">
              <span className="mb-1 block font-medium">
                ID del gerente autorizador *
              </span>
              <input
                type="text"
                value={autorizadoPor}
                onChange={(e) => setAutorizadoPor(e.target.value)}
                placeholder="Ej: GER-001"
                className="w-full rounded-lg border border-slate-300 px-3 py-1.5 text-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
                disabled={isPending}
              />
            </label>
          )}

          {/* Motivo */}
          <label className="block text-sm text-slate-700">
            <span className="mb-1 block font-medium">Motivo del descuento *</span>
            <textarea
              value={motivo}
              onChange={(e) => setMotivo(e.target.value)}
              placeholder="Mínimo 5 caracteres"
              rows={2}
              className="w-full resize-none rounded-lg border border-slate-300 px-3 py-1.5 text-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              disabled={isPending}
            />
          </label>

          {/* Resumen */}
          {porcentajeNum > 0 && (
            <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-600">
                  Descuento ({porcentajeNum}%)
                </span>
                <span
                  className={cn(
                    'font-medium',
                    superaLimite ? 'text-orange-700' : 'text-green-700',
                  )}
                >
                  -{formatoMoneda(montoDescuento)}
                </span>
              </div>
              <div className="mt-1 flex justify-between font-semibold text-slate-900">
                <span>Total final</span>
                <span>{formatoMoneda(totalConDescuento)}</span>
              </div>
            </div>
          )}

          {/* Error del backend dentro del modal (E-05) */}
          {error && (
            <Alert variant="error" title="No se pudo aplicar el descuento" message={error} />
          )}
        </div>

        {/* Botones */}
        <div className="flex gap-3 px-6 pb-6">
          <Button
            variant="secondary"
            className="flex-1"
            onClick={handleReset}
            disabled={isPending}
          >
            Cancelar
          </Button>
          <Button
            className="flex-1 bg-gray-800 hover:bg-gray-900"
            onClick={handleConfirm}
            disabled={!formularioValido || isPending}
          >
            {isPending ? 'Aplicando...' : 'Aplicar'}
          </Button>
        </div>
      </div>
    </div>
  );
}
