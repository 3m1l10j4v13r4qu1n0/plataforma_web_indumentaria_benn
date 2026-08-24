import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RegistrarCambioPage } from '@/pages/cambios/RegistrarCambioPage';
import type {
  CambioResponse,
  MarcarEnCambioResponse,
  ValidarTicketResponse,
} from '@/types/api';

vi.mock('@/api/services/venta.service', () => ({
  ventaService: {
    procesarVenta: vi.fn(),
    validarTicket: vi.fn(),
    marcarVentaEnCambio: vi.fn(),
  },
}));

vi.mock('@/api/services/cambio.service', () => ({
  cambioService: {
    procesarCambio: vi.fn(),
    validarEstadoProducto: vi.fn(),
  },
}));

import { ventaService } from '@/api/services/venta.service';
import { cambioService } from '@/api/services/cambio.service';

const mockValidarTicket = vi.mocked(ventaService.validarTicket);
const mockMarcarVentaEnCambio = vi.mocked(ventaService.marcarVentaEnCambio);
const mockProcesarCambio = vi.mocked(cambioService.procesarCambio);
const mockValidarEstado = vi.mocked(cambioService.validarEstadoProducto);

/** Error con la forma que normalizarErrorApi interpreta como respuesta del backend. */
function crearErrorApi(data: Record<string, unknown>) {
  return { isAxiosError: true, response: { status: 400, data } };
}

const compraValida: ValidarTicketResponse = {
  existe: true,
  venta_original_id: 'V-999',
  numero_ticket: 'T-20260601-001',
  fecha_compra: '2026-08-10T14:30:00',
  cajero_original_id: 'C-003',
  items: [
    { producto_id: '123', nombre: 'Camiseta Azul', cantidad: 1, precio: 25 },
    { producto_id: '124', nombre: 'Jean Recto', cantidad: 2, precio: 40 },
  ],
  mensaje: 'Ticket válido. Puede continuar con el proceso de cambio.',
};

const retencionOk: MarcarEnCambioResponse = {
  numero_ticket: 'T-20260601-001',
  estado: 'EN_CAMBIO',
  mensaje: 'Venta marcada como EN_CAMBIO.',
};

const cambioRegistrado: CambioResponse = {
  id: 'CMB-123',
  venta_original_id: 'V-999',
  fecha_cambio: '2026-08-23T15:00:00',
  cajero_id: 'C-005',
  producto_a_cambiar_id: '123',
  nuevo_producto_id: '124',
  estado: 'APROBADO',
  motivo: 'Talla incorrecta',
};

async function buscarTicket(user: ReturnType<typeof userEvent.setup>) {
  await user.type(
    screen.getByLabelText('Buscar ticket por número'),
    'T-20260601-001',
  );
  await user.keyboard('{Enter}');
}

/** Paso 2: selecciona un producto de la compra y retiene el ticket. */
async function retenerTicket(user: ReturnType<typeof userEvent.setup>) {
  await user.click(
    await screen.findByLabelText('Seleccionar Camiseta Azul para cambiar'),
  );
  await user.click(screen.getByRole('button', { name: 'Iniciar cambio' }));
}

/** Paso 3: completa y envía el formulario de registro del cambio. */
async function completarRegistroCambio(
  user: ReturnType<typeof userEvent.setup>,
) {
  await user.type(
    screen.getByLabelText('ID del cajero que procesa el cambio'),
    'C-005',
  );
  await user.type(
    screen.getByLabelText('ID del nuevo producto de reemplazo'),
    '124',
  );
  await user.type(
    screen.getByLabelText('Motivo del cambio'),
    'Talla incorrecta',
  );
  await user.click(screen.getByRole('button', { name: 'Registrar cambio' }));
}

function renderizar() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <RegistrarCambioPage />
    </QueryClientProvider>,
  );
}

describe('RegistrarCambioPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('HU-04: muestra un mensaje amigable cuando el ticket no existe', async () => {
    const user = userEvent.setup();
    mockValidarTicket.mockRejectedValue(
      crearErrorApi({
        existe: false,
        error: 'TICKET_NO_ENCONTRADO',
        mensaje: 'El número de ticket ingresado no existe en el sistema.',
      }),
    );
    renderizar();

    await buscarTicket(user);

    expect(
      await screen.findByText(
        'El número de ticket no existe en el sistema. Verificá el comprobante.',
      ),
    ).toBeInTheDocument();
  });

  it('HU-04: al validar un ticket muestra los datos de la compra original', async () => {
    const user = userEvent.setup();
    mockValidarTicket.mockResolvedValue(compraValida);
    renderizar();

    await buscarTicket(user);

    expect(await screen.findByText('Compra Original')).toBeInTheDocument();
    expect(screen.getByText('T-20260601-001')).toBeInTheDocument();
    expect(screen.getByText('Camiseta Azul')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Iniciar cambio' })).toBeDisabled();
  });

  it('completa el flujo: retiene el ticket, registra el cambio y valida el estado', async () => {
    const user = userEvent.setup();
    mockValidarTicket.mockResolvedValue(compraValida);
    mockMarcarVentaEnCambio.mockResolvedValue(retencionOk);
    mockProcesarCambio.mockResolvedValue(cambioRegistrado);
    mockValidarEstado.mockResolvedValue({
      mensaje: 'Producto validado correctamente. Puede continuar con el cambio.',
      es_apto_para_cambio: true,
    });
    renderizar();

    await buscarTicket(user);

    // Paso 2: retener el ticket
    await user.click(
      screen.getByLabelText('Seleccionar Camiseta Azul para cambiar'),
    );
    await user.click(screen.getByRole('button', { name: 'Iniciar cambio' }));
    expect(await screen.findByText('EN_CAMBIO')).toBeInTheDocument();
    expect(mockMarcarVentaEnCambio).toHaveBeenCalledWith('T-20260601-001');

    // Paso 3: registrar el cambio
    await completarRegistroCambio(user);
    expect(await screen.findByText('Cambio Registrado')).toBeInTheDocument();
    expect(mockProcesarCambio).toHaveBeenCalledWith({
      venta_original_id: 'V-999',
      cajero_id: 'C-005',
      producto_a_cambiar_id: '123',
      nuevo_producto_id: '124',
      motivo: 'Talla incorrecta',
    });

    // Paso 4: inspección física apta
    await user.click(screen.getByLabelText('Nuevo con etiqueta'));
    await user.click(
      screen.getByLabelText('El producto conserva su etiqueta original'),
    );
    await user.click(
      screen.getByRole('button', { name: 'Confirmar inspección' }),
    );

    expect(
      await screen.findByText(
        'Producto validado correctamente. Puede continuar con el cambio.',
      ),
    ).toBeInTheDocument();
    expect(mockValidarEstado).toHaveBeenCalledWith('CMB-123', {
      producto_id: '123',
      estado_producto: 'NUEVO_ETIQUETADO',
      tiene_etiqueta: true,
      observaciones: null,
      cajero_id: 'C-005',
    });
  });

  it('HU-02: muestra rechazo cuando el plazo de 15 días está vencido', async () => {
    const user = userEvent.setup();
    mockValidarTicket.mockResolvedValue(compraValida);
    mockMarcarVentaEnCambio.mockResolvedValue(retencionOk);
    mockProcesarCambio.mockRejectedValue(
      crearErrorApi({
        error: 'PLAZO_VENCIDO',
        mensaje: 'Pasaron 20 días desde la compra (límite: 15).',
      }),
    );
    renderizar();

    await buscarTicket(user);
    await retenerTicket(user);
    await completarRegistroCambio(user);

    expect(
      await screen.findByText(
        'Pasaron más de 15 días desde la compra. El cambio fue rechazado.',
      ),
    ).toBeInTheDocument();
    expect(screen.queryByText('Cambio Registrado')).not.toBeInTheDocument();
  });

  it('HU-03: muestra rechazo cuando el producto no es apto para el cambio', async () => {
    const user = userEvent.setup();
    mockValidarTicket.mockResolvedValue(compraValida);
    mockMarcarVentaEnCambio.mockResolvedValue(retencionOk);
    mockProcesarCambio.mockResolvedValue(cambioRegistrado);
    mockValidarEstado.mockRejectedValue(
      crearErrorApi({
        error: 'PRODUCTO_NO_APTO',
        mensaje: 'El producto no cumple las condiciones para ser cambiado.',
        motivo: 'PRODUCTO_USADO',
        es_apto_para_cambio: false,
      }),
    );
    renderizar();

    await buscarTicket(user);
    await retenerTicket(user);
    await completarRegistroCambio(user);

    // Producto usado: obliga a completar observaciones antes de enviar
    await user.click(screen.getByLabelText('Usado'));
    expect(
      screen.getByRole('button', { name: 'Confirmar inspección' }),
    ).toBeDisabled();

    await user.type(
      screen.getByLabelText('Observaciones de la inspección'),
      'Presenta señales claras de uso',
    );
    await user.click(
      screen.getByRole('button', { name: 'Confirmar inspección' }),
    );

    expect(
      await screen.findByText(
        'El producto no cumple las condiciones para ser cambiado (debe estar nuevo y con etiqueta).',
      ),
    ).toBeInTheDocument();
  });
});
