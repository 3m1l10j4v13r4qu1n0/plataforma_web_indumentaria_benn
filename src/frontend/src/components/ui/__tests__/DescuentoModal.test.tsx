import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { DescuentoModal } from '@/components/ui';

interface Props {
  error?: string | null;
}

function renderizar(props: Props = {}) {
  return render(
    <DescuentoModal
      isOpen
      onClose={vi.fn()}
      onConfirm={vi.fn()}
      totalVenta={110}
      isPending={false}
      {...props}
    />,
  );
}

async function completarFormulario(porcentaje: string) {
  const user = userEvent.setup();
  await user.type(screen.getByLabelText(/Descuento \(%\)/), porcentaje);
  await user.type(
    screen.getByLabelText('Motivo del descuento *'),
    'Cliente frecuente',
  );
  return user;
}

describe('DescuentoModal', () => {
  it('muestra el hint del límite contractual', () => {
    renderizar();

    expect(
      screen.getByText('(Máx. 20% sin autorización)'),
    ).toBeInTheDocument();
  });

  it('no exige autorización cuando el descuento está dentro del límite (E-04)', async () => {
    const onConfirm = vi.fn();
    render(
      <DescuentoModal
        isOpen
        onClose={vi.fn()}
        onConfirm={onConfirm}
        totalVenta={110}
        isPending={false}
      />,
    );

    expect(screen.queryByText('Autorización Requerida')).not.toBeInTheDocument();

    const user = await completarFormulario('10');
    await user.click(screen.getByRole('button', { name: 'Aplicar' }));

    expect(onConfirm).toHaveBeenCalledWith({
      porcentaje: 10,
      motivo: 'Cliente frecuente',
      autorizado_por: null,
    });
  });

  it('muestra el header naranja y exige gerente al superar el límite (contrato HU-05)', async () => {
    renderizar();

    const user = userEvent.setup();
    await user.type(screen.getByLabelText(/Descuento \(%\)/), '40');
    await user.type(
      screen.getByLabelText('Motivo del descuento *'),
      'Cliente frecuente',
    );

    expect(screen.getByText('Autorización Requerida')).toBeInTheDocument();
    expect(
      screen.getByText(
        'El descuento del 40% supera el límite permitido (20%).',
      ),
    ).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Aplicar' })).toBeDisabled();

    await user.type(screen.getByLabelText('ID del gerente autorizador *'), 'GER-001');
    expect(screen.getByRole('button', { name: 'Aplicar' })).toBeEnabled();
  });

  it('muestra el error del backend dentro del modal (E-05)', () => {
    renderizar({ error: 'El descuento requiere la autorización de un gerente.' });

    expect(
      screen.getByText('No se pudo aplicar el descuento'),
    ).toBeInTheDocument();
    expect(
      screen.getByText('El descuento requiere la autorización de un gerente.'),
    ).toBeInTheDocument();
  });
});
