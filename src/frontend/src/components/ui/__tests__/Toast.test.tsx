import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Toast } from '@/components/ui';

describe('Toast (HU-08)', () => {
  it('muestra el mensaje de éxito verde requerido', () => {
    render(<Toast message="Operación exitosa. Inventario actualizado" onDismiss={vi.fn()} />);

    expect(
      screen.getByText('Operación exitosa. Inventario actualizado'),
    ).toBeInTheDocument();
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('se auto-descarta tras la duración configurada', () => {
    vi.useFakeTimers();
    const onDismiss = vi.fn();
    render(<Toast message="Hola" duration={1000} onDismiss={onDismiss} />);

    expect(onDismiss).not.toHaveBeenCalled();
    vi.advanceTimersByTime(1100);
    expect(onDismiss).toHaveBeenCalledTimes(1);
    vi.useRealTimers();
  });

  it('permite cerrarlo manualmente', async () => {
    const user = userEvent.setup();
    const onDismiss = vi.fn();
    render(<Toast message="Hola" onDismiss={onDismiss} />);

    await user.click(screen.getByLabelText('Cerrar notificación'));
    expect(onDismiss).toHaveBeenCalledTimes(1);
  });
});
