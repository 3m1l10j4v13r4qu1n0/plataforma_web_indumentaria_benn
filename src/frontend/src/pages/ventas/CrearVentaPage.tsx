import { useEffect, useState } from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import {
  StockSearchInput,
  VentaProductoCard,
  VentaItemRow,
  TicketCard,
  DescuentoModal,
  Button,
  Alert,
  type VentaItem,
} from '@/components/ui';
import { useStockProducto } from '@/hooks/useStockProducto';
import { useVenta } from '@/hooks/useVenta';
import { useDescuento } from '@/hooks/useDescuento';
import { normalizarErrorApi } from '@/utils/apiErrors';
import { formatoFechaCorta, formatoMoneda } from '@/utils/format';
import type { CrearVentaRequest } from '@/types/api';

/**
 * HU-01 / HU-07 — Nueva venta y generación de ticket.
 *
 * Orquesta:
 * 1. Búsqueda del producto por código → muestra stock disponible.
 * 2. Agregado de items con cantidad al carrito ("Productos a vender").
 * 3. Bloqueo preventivo si un ítem quedó sin stock (contrato HU-01).
 * 4. Confirmación de la venta vía POST /ventas.
 * 5. Visualización del ticket generado con opción a imprimir.
 *
 * Textos según contrato visual (docs/05_mockups/mockup_hu01.html).
 *
 * SRP: solo orquesta; la lógica de negocio queda en hooks/servicios.
 */
export function CrearVentaPage() {
  const [inputCodigo, setInputCodigo] = useState('');
  const [codigoBuscado, setCodigoBuscado] = useState('');
  const [cantidad, setCantidad] = useState(1);
  const [items, setItems] = useState<VentaItem[]>([]);
  const [vendedorId, setVendedorId] = useState('V-001');
  const [descuentoModalAbierto, setDescuentoModalAbierto] = useState(false);

  const stockQuery = useStockProducto(codigoBuscado);  const ventaMutation = useVenta();
  const descuentoMutation = useDescuento();

  /**
   * Busca el stock del código ingresado. Si se vuelve a escanear el mismo
   * código, fuerza un refetch para re-consultar el stock vigente en vez de
   * servir la respuesta cacheada.
   */
  const buscarProducto = (codigo: string) => {
    if (codigo === codigoBuscado) {
      void stockQuery.refetch();
    } else {
      setCodigoBuscado(codigo);
    }
  };

  const producto = stockQuery.data;
  const hayItems = items.length > 0;
  const ventaExitosa = ventaMutation.data;
  const totalArticulos = items.reduce((acc, i) => acc + i.cantidad, 0);
  const totalPagar = items.reduce((acc, i) => acc + i.precio * i.cantidad, 0);

  /** Ítem sin stock que bloquea la venta (estado bloqueado del contrato). */
  const itemSinStock = items.find((i) => i.stockActual === 0);
  const ventaBloqueada = Boolean(itemSinStock);

  /**
   * Sincroniza el stock de los ítems del carrito con la última consulta
   * del producto: si el stock cambió después de agregarlo, la fila queda
   * desactualizada y dispara el bloqueo preventivo del contrato.
   */
  useEffect(() => {
    if (!producto) return;
    setItems((prev) =>
      prev.map((i) =>
        i.productoId === producto.productoId
          ? { ...i, stockActual: producto.stockActual }
          : i,
      ),
    );
  }, [producto]);

  const agregarItem = () => {
    if (!producto || cantidad < 1) return;

    setItems((prev) => {
      const existente = prev.find((i) => i.productoId === producto.productoId);
      if (existente) {
        return prev.map((i) =>
          i.productoId === producto.productoId
            ? { ...i, cantidad: i.cantidad + cantidad }
            : i,
        );
      }
      return [
        ...prev,
        {
          productoId: producto.productoId,
          nombre: producto.nombre,
          precio: producto.precio,
          cantidad,
          stockActual: producto.stockActual,
        },
      ];
    });
    setCantidad(1);
  };

  const cambiarCantidadItem = (productoId: string, nuevaCantidad: number) => {
    setItems((prev) =>
      prev.map((i) =>
        i.productoId === productoId ? { ...i, cantidad: nuevaCantidad } : i,
      ),
    );
  };

  const quitarItem = (productoId: string) => {
    setItems((prev) => prev.filter((i) => i.productoId !== productoId));
  };

  const cancelarVenta = () => {
    setItems([]);
    setCodigoBuscado('');
    setInputCodigo('');
    setCantidad(1);
  };

  const confirmarVenta = () => {
    if (ventaBloqueada) return;

    const request: CrearVentaRequest = {
      vendedor_id: vendedorId.trim() || 'V-001',
      items: items.map((i) => ({
        producto_id: i.productoId,
        cantidad: i.cantidad,
      })),
    };
    ventaMutation.mutate(request, {
      onSuccess: () => {
        setItems([]);
        setCodigoBuscado('');
        setInputCodigo('');
        setCantidad(1);
      },
    });
  };

  const imprimirTicket = () => {
    window.print();
  };

  const cerrarTicket = () => {
    ventaMutation.reset();
  };

  const confirmarDescuento = (datos: {
    porcentaje: number;
    motivo: string;
    autorizado_por: string | null;
  }) => {
    if (!ventaExitosa) return;

    descuentoMutation.mutate(
      {
        venta_id: ventaExitosa.id,
        porcentaje: datos.porcentaje,
        motivo: datos.motivo,
        autorizado_por: datos.autorizado_por,
      },
      {
        onSuccess: () => {
          setDescuentoModalAbierto(false);
        },
      },
    );
  };

  const errorConfirmacion = ventaMutation.error
    ? normalizarErrorApi(ventaMutation.error)
    : null;

  const errorDescuento = descuentoMutation.error
    ? normalizarErrorApi(descuentoMutation.error)
    : null;

  return (
    <main className="min-h-screen bg-slate-50 p-6">
      <PageHeader
        title="Nueva Venta"
        meta={{ label: 'Vendedor', value: vendedorId }}
        timestamp={formatoFechaCorta(new Date())}
      />

      {/* HU-07: vista post-venta según contrato (card centrada) */}
      {ventaExitosa ? (
        <div className="mx-auto flex max-w-md flex-col gap-4">
          <TicketCard
            venta={ventaExitosa}
            onImprimir={imprimirTicket}
            onCerrar={cerrarTicket}
          />

          {/* HU-05: Botón para aplicar descuento */}
          {!descuentoMutation.data && (
            <Button
              variant="secondary"
              className="w-full"
              onClick={() => setDescuentoModalAbierto(true)}
            >
              Aplicar descuento
            </Button>
          )}

          {/* Descuento aplicado */}
          {descuentoMutation.data && (
            <div className="rounded-lg border-l-4 border-green-500 bg-green-50 p-4">
              <p className="text-sm font-semibold text-green-800">
                Descuento aplicado
              </p>
              <p className="mt-1 text-sm text-green-700">
                {descuentoMutation.data.mensaje}
              </p>
            </div>
          )}
        </div>
      ) : (
        <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
        {/* Columna izquierda: búsqueda + producto */}
        <section className="space-y-4">
          <StockSearchInput
            value={inputCodigo}
            onValueChange={setInputCodigo}
            onSearch={buscarProducto}
            label="Buscar o escanear producto"
            placeholder="Ej: CAM-001 o 'Camiseta Básica'"
            disabled={ventaMutation.isPending}
          />

          {stockQuery.isPending && (
            <div className="rounded-lg border border-slate-200 bg-white p-4 text-sm text-slate-500">
              Consultando stock...
            </div>
          )}

          {stockQuery.isError && (
            <Alert
              variant="error"
              title="Producto no encontrado"
              message={normalizarErrorApi(stockQuery.error)}
            />
          )}

          {producto && (
            <VentaProductoCard
              producto={producto}
              cantidad={cantidad}
              onCantidadChange={setCantidad}
              onAgregar={agregarItem}
              yaAgregado={items.some(
                (i) => i.productoId === producto.productoId,
              )}
            />
          )}
        </section>

        {/* Columna derecha: carrito "Productos a vender" */}
        <aside className="space-y-4">
          <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-lg sm:p-5">
            <h2 className="mb-3 text-sm font-bold uppercase tracking-wide text-slate-500">
              Productos a vender
            </h2>

            {!hayItems ? (
              <p className="text-sm text-slate-500">
                Todavía no hay productos agregados.
              </p>
            ) : (
              <div className="-mx-4 overflow-x-auto sm:-mx-5">
                <table className="w-full text-left">
                  <thead>
                    <tr className="border-b border-slate-200">
                      <th className="px-4 py-2 text-xs font-medium uppercase text-slate-500 sm:px-5">
                        Producto
                      </th>
                      <th className="px-4 py-2 text-xs font-medium uppercase text-slate-500 sm:px-5">
                        Precio Unit.
                      </th>
                      <th className="px-4 py-2 text-xs font-medium uppercase text-slate-500 sm:px-5">
                        Stock Actual
                      </th>
                      <th className="px-4 py-2 text-xs font-medium uppercase text-slate-500 sm:px-5">
                        Cantidad
                      </th>
                      <th className="px-4 py-2 text-xs font-medium uppercase text-slate-500 sm:px-5">
                        Subtotal
                      </th>
                      <th aria-label="Acciones" />
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {items.map((item) => (
                      <VentaItemRow
                        key={item.productoId}
                        item={item}
                        onCantidadChange={(nuevaCantidad) =>
                          cambiarCantidadItem(item.productoId, nuevaCantidad)
                        }
                        onQuitar={() => quitarItem(item.productoId)}
                      />
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {hayItems && (
              <>
                <div className="mt-4 flex items-center justify-between border-t border-slate-200 pt-3 text-sm text-slate-600">
                  <span>Total de artículos</span>
                  <span>{totalArticulos}</span>
                </div>
                <p className="mt-1 flex items-baseline justify-between">
                  <span className="text-sm font-semibold text-slate-900">
                    Total a Pagar
                  </span>
                  <span className="text-3xl font-bold text-brand-700">
                    {formatoMoneda(totalPagar)}
                  </span>
                </p>

                <label className="mt-4 block text-sm text-slate-700">
                  <span className="mb-1 block">ID de vendedor</span>
                  <input
                    type="text"
                    value={vendedorId}
                    onChange={(e) => setVendedorId(e.target.value)}
                    className="w-full rounded-lg border border-slate-300 px-3 py-1.5 text-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
                    aria-label="ID de vendedor"
                  />
                </label>

                {/* Bloqueo preventivo por ítem sin stock (contrato HU-01) */}
                {ventaBloqueada && itemSinStock && (
                  <Alert
                    variant="error"
                    className="mt-4"
                    title="No se puede procesar la venta"
                    message={`El producto "${itemSinStock.nombre}" no tiene stock disponible. Por favor, elimínalo del carrito para continuar.`}
                  />
                )}
              </>
            )}

            <div className="mt-4 flex gap-3">
              <Button
                type="button"
                variant="secondary"
                className="flex-1"
                disabled={!hayItems || ventaMutation.isPending}
                onClick={cancelarVenta}
              >
                Cancelar
              </Button>
              <Button
                type="button"
                className="flex-1"
                disabled={
                  !hayItems || ventaBloqueada || ventaMutation.isPending
                }
                onClick={confirmarVenta}
              >
                {ventaMutation.isPending ? (
                  <>
                    <svg
                      className="h-4 w-4 animate-spin"
                      viewBox="0 0 24 24"
                      fill="none"
                      aria-hidden="true"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                      />
                    </svg>
                    Procesando...
                  </>
                ) : (
                  <>
                    {ventaBloqueada && (
                      <svg
                        className="h-4 w-4"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth={2}
                        viewBox="0 0 24 24"
                        aria-hidden="true"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                        />
                      </svg>
                    )}
                    Confirmar Venta
                  </>
                )}
              </Button>
            </div>
          </div>

          {errorConfirmacion && (
            <Alert
              variant="error"
              title="No se pudo completar la venta"
              message={errorConfirmacion}
            />
          )}
        </aside>
        </div>
      )}

      {/* HU-05: Modal de descuento */}
      <DescuentoModal
        isOpen={descuentoModalAbierto}
        onClose={() => {
          setDescuentoModalAbierto(false);
          if (descuentoMutation.isError) descuentoMutation.reset();
        }}
        onConfirm={confirmarDescuento}
        totalVenta={ventaExitosa?.total ?? 0}
        isPending={descuentoMutation.isPending}
        error={errorDescuento}
      />
    </main>
  );
}