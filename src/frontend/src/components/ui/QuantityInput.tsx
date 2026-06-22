import { cn } from '@/utils/cn';

interface QuantityInputProps {
  /** Valor actual de la cantidad */
  value: number;
  /** Callback cuando cambia la cantidad */
  onChange: (value: number) => void;
  /** Cantidad mínima permitida (default: 1) */
  min?: number;
  /** Cantidad máxima permitida (stock disponible) */
  max: number;
  /** Si está deshabilitado */
  disabled?: boolean;
  /** Si hay error de validación */
  hasError?: boolean;
  /** Clase CSS adicional */
  className?: string;
}

/**
 * Input numérico para ajustar la cantidad de un producto en el carrito.
 *
 * 🎯 Características:
 * - Valida rango [min, max]
 * - Muestra estado de error visual
 * - Accesible (ARIA labels)
 *
 * SRP: Solo maneja la UI del input, no la lógica de validación del carrito.
 */
export function QuantityInput({
  value,
  onChange,
  min = 1,
  max,
  disabled = false,
  hasError = false,
  className,
}: QuantityInputProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const raw = e.target.value;
    if (raw === '') {
      onChange(0);
      return;
    }
    const parsed = parseInt(raw, 10);
    if (!Number.isNaN(parsed)) {
      onChange(parsed);
    }
  };

  const handleBlur = () => {
    // Normaliza el valor al salir del input
    if (value < min) onChange(min);
    if (value > max) onChange(max);
  };

  const handleIncrement = () => {
    if (value < max) onChange(value + 1);
  };

  const handleDecrement = () => {
    if (value > min) onChange(value - 1);
  };

  return (
    <div className={cn('inline-flex items-center', className)}>
      <button
        type="button"
        onClick={handleDecrement}
        disabled={disabled || value <= min}
        className={cn(
          'flex h-8 w-8 items-center justify-center rounded-l-md border border-slate-300',
          'bg-white text-slate-600 transition-colors',
          'hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50',
        )}
        aria-label="Disminuir cantidad"
      >
        −
      </button>

      <input
        type="number"
        value={value}
        onChange={handleChange}
        onBlur={handleBlur}
        min={min}
        max={max}
        disabled={disabled}
        className={cn(
          'h-8 w-14 border-y border-slate-300 px-2 text-center text-sm font-medium',
          'focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500',
          'disabled:cursor-not-allowed disabled:bg-slate-50',
          '[appearance:textfield] [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none',
          hasError && 'border-rose-500 bg-rose-50 text-rose-900',
          !hasError && 'text-slate-900',
        )}
        aria-label="Cantidad a vender"
      />

      <button
        type="button"
        onClick={handleIncrement}
        disabled={disabled || value >= max}
        className={cn(
          'flex h-8 w-8 items-center justify-center rounded-r-md border border-slate-300',
          'bg-white text-slate-600 transition-colors',
          'hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50',
        )}
        aria-label="Aumentar cantidad"
      >
        +
      </button>
    </div>
  );
}
