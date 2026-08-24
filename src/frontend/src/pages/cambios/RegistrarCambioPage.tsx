import { useState } from 'react';
import {
  Alert,
  CambioExitosoCard,
  CompraOriginalCard,
  EstadoProductoSelector,
  RegistroCambioForm,
  TicketSearchInput,
  type RegistroCambioFormValues,
  type ValidarEstadoFormValues,
} from '@/components/ui';
import { useMarcarVentaEnCambio } from '@/hooks/useMarcarVentaEnCambio';
import { useRegistrarCambio, useValidarEstadoProducto } from '@/hooks/useCambio';
import { useTicket } from '@/hooks/useTicket';
import { normalizarErrorApi } from '@/utils/apiErrors';

const INSPECCION_INICIAL: ValidarEstadoFormValues = {
  estadoProducto: null,
  tieneEtiqueta: false,
  observaciones: '',
};

/**
 * HU-04 + HU-02 + HU-03 — Flujo unificado de cambios de productos.
 *
 * Secuencia espejo del backend:
 * 1. Buscar el ticket de compra (GET validar-ticket)
 * 2. Retener el ticket como EN_CAMBIO (PATCH estado)
 * 3. Registrar el cambio con validación de plazo (POST /cambios)
 * 4. Validar el estado físico del producto (POST validar-estado)
 *
 * SRP: Orquesta hooks + componentes presentacionales; sin llamadas HTTP propias.
 */
export function RegistrarCambioPage() {
  const [productoSeleccionadoId, setProductoSeleccionadoId] = useState<
    string | null
  >(null);
  const [cajeroRegistrado, setCajeroRegistrado] = useState('');
  const [inspeccion, setInspeccion] =
    useState<ValidarEstadoFormValues>(INSPECCION_INICIAL);
  const [mensajeInspeccionExitosa, setMensajeInspeccionExitosa] = useState<
    string | null
  >(null);

  const ticket = useTicket();
  const retener = useMarcarVentaEnCambio();
  const registrar = useRegistrarCambio();
  const validarEstado = useValidarEstadoProducto();

  const compra = ticket.compra;
  const cambio = registrar.data ?? null;
  const ticketRetenido = retener.isSuccess;

  const errorBusqueda =
    ticket.buscoAlMenosUnaVez && ticket.error ? ticket.error : null;
  const errorRetencion = retener.error
    ? normalizarErrorApi(retener.error)
    : null;
  const errorRegistro = registrar.error
    ? normalizarErrorApi(registrar.error)
    : null;
  const errorInspeccion = validarEstado.error
    ? normalizarErrorApi(validarEstado.error)
    : null;

  const productoSeleccionado =
    compra?.items.find((item) => item.producto_id === productoSeleccionadoId) ??
    null;

  const handleRegistrarCambio = (values: RegistroCambioFormValues) => {
    if (!compra || !productoSeleccionadoId) return;
    setCajeroRegistrado(values.cajeroId);
    registrar.mutate({
      venta_original_id: compra.venta_original_id,
      cajero_id: values.cajeroId,
      producto_a_cambiar_id: productoSeleccionadoId,
      nuevo_producto_id: values.nuevoProductoId,
      motivo: values.motivo || null,
    });
  };

  const handleConfirmarInspeccion = () => {
    if (!cambio || !inspeccion.estadoProducto || !productoSeleccionadoId) return;
    validarEstado.mutate(
      {
        cambioId: cambio.id,
        request: {
          producto_id: productoSeleccionadoId,
          estado_producto: inspeccion.estadoProducto,
          tiene_etiqueta: inspeccion.tieneEtiqueta,
          observaciones: inspeccion.observaciones || null,
          cajero_id: cajeroRegistrado || null,
        },
      },
      {
        onSuccess: (resultado) => setMensajeInspeccionExitosa(resultado.mensaje),
      },
    );
  };

  const handleNuevoCambio = () => {
    ticket.reiniciar();
    retener.reset();
    registrar.reset();
    validarEstado.reset();
    setProductoSeleccionadoId(null);
    setCajeroRegistrado('');
    setInspeccion(INSPECCION_INICIAL);
    setMensajeInspeccionExitosa(null);
  };

  return (
    <main className="min-h-screen bg-slate-50 p-6">
      <header className="mb-6">
        <h1 className="text-2xl font-bold text-slate-800">
          Registrar Cambio de Producto
        </h1>
        <p className="text-sm text-slate-500">
          Buscá el ticket de compra, registrá el cambio y validá el estado del
          producto.
        </p>
      </header>

      {/* Paso 1: Búsqueda del ticket (HU-04) */}
      <section aria-label="Buscar ticket de compra">
        <TicketSearchInput
          value={ticket.numeroTicket}
          onValueChange={ticket.setNumeroTicket}
          onSearch={ticket.buscarTicket}
          disabled={!ticket.isLoading && Boolean(compra)}
        />
        {ticket.isLoading && (
          <div className="mt-4 flex items-center gap-3 py-2">
            <div className="h-6 w-6 animate-spin rounded-full border-4 border-slate-300 border-t-brand-600" />
            <span className="text-sm text-slate-500">Buscando ticket...</span>
          </div>
        )}
        {errorBusqueda && (
          <Alert
            variant="error"
            title="Ticket no válido"
            message={errorBusqueda}
            className="mt-4"
          />
        )}
      </section>

      {/* Paso 2: Selección del producto y retención del ticket (HU-04) */}
      {compra && !cambio && (
        <>
          <CompraOriginalCard
            compra={compra}
            itemSeleccionadoId={productoSeleccionadoId}
            onSeleccionarItem={setProductoSeleccionadoId}
            onIniciarCambio={() => retener.mutate(compra.numero_ticket)}
            retencionEnCurso={retener.isPending}
            ticketRetenido={ticketRetenido}
            className="mt-6"
          />
          {errorRetencion && (
            <Alert
              variant="error"
              title="No se pudo retener el ticket"
              message={errorRetencion}
              className="mt-4"
            />
          )}
        </>
      )}

      {/* Paso 3: Registro del cambio con validación de plazo (HU-02) */}
      {ticketRetenido && !cambio && (
        <>
          <RegistroCambioForm
            productoACambiar={productoSeleccionado}
            onSubmit={handleRegistrarCambio}
            isPending={registrar.isPending}
            className="mt-6"
          />
          {errorRegistro && (
            <Alert
              variant="error"
              title="El cambio fue rechazado"
              message={errorRegistro}
              className="mt-4"
            />
          )}
        </>
      )}

      {/* Paso 4: Confirmación e inspección física (HU-03) */}
      {cambio && (
        <>
          {mensajeInspeccionExitosa && (
            <Alert
              variant="success"
              title="Inspección completada"
              message={mensajeInspeccionExitosa}
              className="mt-6"
            />
          )}
          <CambioExitosoCard cambio={cambio} onNuevoCambio={handleNuevoCambio} className="mt-6" />
          {!mensajeInspeccionExitosa && (
            <>
              <EstadoProductoSelector
                value={inspeccion}
                onChange={setInspeccion}
                onSubmit={handleConfirmarInspeccion}
                isPending={validarEstado.isPending}
                className="mt-6"
              />
              {errorInspeccion && (
                <Alert
                  variant="error"
                  title="El producto no pasó la inspección"
                  message={errorInspeccion}
                  className="mt-4"
                />
              )}
            </>
          )}
        </>
      )}
    </main>
  );
}
