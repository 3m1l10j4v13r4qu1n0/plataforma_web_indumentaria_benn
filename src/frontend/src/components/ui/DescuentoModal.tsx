import { useState } from 'react';
import { Button } from './Button';
import { Alert } from './Alert';
import { cn } from '@/utils/cn';

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
}

/**
 * Modal para aplicar descuentos a una venta (HU-05).
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
        className="absolute inset-0 bg-black/50"
        onClick={handleReset}
        aria-hidden="true"
      />

      {/* Modal */}
      <div className="relative mx-4 w-full max-w-md rounded-xl border border-slate-200 bg-white p-6 shadow-xl">
        <h2 className="text-lg font-semibold text-slate-900">
          Aplicar descuento
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          Total de la venta: <span className="font-medium">${totalVenta}</span>
        </p>

        <div className="mt-4 space-y-4">
          {/* Porcentaje */}
          <label className="block text-sm text-slate-700">
            <span className="mb-1 block">Porcentaje de descuento</span>
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
                    ? 'border-amber-400 focus:border-amber-500 focus:ring-amber-500/20'
                    : 'border-slate-300 focus:border-brand-500 focus:ring-brand-500/20',
                )}
                disabled={isPending}
              />
              <span className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-slate-400">
                %
              </span>
            </div>
          </label>

          {/* Alerta de límite */}
          {superaLimite && (
            <Alert
              variant="warning"
              title="Requiere autorización"
              message={`El descuento de ${porcentajeNum}% supera el límite de ${LIMITE_SIN_AUTORIZACION}%. Se requiere la autorización de un gerente.`}
            />
          )}

          {/* Campo de autorización (condicional) */}
          {superaLimite && (
            <label className="block text-sm text-slate-700">
              <span className="mb-1 block">ID del gerente autorizador *</span>
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
            <span className="mb-1 block">Motivo del descuento *</span>
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
              <div className="flex justify-between text-slate-600">
                <span>Descuento ({porcentajeNum}%)</span>
                <span className="font-medium text-rose-600">
                  -${montoDescuento.toFixed(2)}
                </span>
              </div>
              <div className="mt-1 flex justify-between font-semibold text-slate-900">
                <span>Total final</span>
                <span>${totalConDescuento.toFixed(2)}</span>
              </div>
            </div>
          )}
        </div>

        {/* Botones */}
        <div className="mt-6 flex gap-3">
          <Button
            variant="secondary"
            className="flex-1"
            onClick={handleReset}
            disabled={isPending}
          >
            Cancelar
          </Button>
          <Button
            className="flex-1"
            onClick={handleConfirm}
            disabled={!formularioValido || isPending}
          >
            {isPending ? 'Aplicando...' : 'Aplicar descuento'}
          </Button>
        </div>
      </div>
    </div>
  );
}
