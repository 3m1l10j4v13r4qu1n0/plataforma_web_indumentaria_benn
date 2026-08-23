import { useState } from 'react';
import { PageHeader } from '@/components/layout/PageHeader';
import {
  StockSearchInput,
  VentaProductoCard,
  VentaItemRow,
  TicketCard,
  Button,
  Alert,
  type VentaItem,
} from '@/components/ui';
import { useStockProducto } from '@/hooks/useStockProducto';
import { useVenta } from '@/hooks/useVenta';
import { normalizarErrorApi } from '@/utils/apiErrors';
import type { CrearVentaRequest } from '@/types/api';

/**
 * HU-01 / HU-07 — Procesar venta y generar ticket.
 *
 * Orquesta:
 * 1. Búsqueda del producto por código → muestra stock disponible.
 * 2. Agregado de items con cantidad al carrito de venta.
 * 3. Confirmación de la venta vía POST /ventas.
 * 4. Visualización del ticket generado con opción a imprimir.
 * 5. Manejo de estados Loading / Error / Success.
 *
 * SRP: solo orquesta; la lógica de negocio queda en hooks/servicios.
 */
export function CrearVentaPage() {
  const [inputCodigo, setInputCodigo] = useState('');
  const [codigoBuscado, setCodigoBuscado] = useState('');
  const [cantidad, setCantidad] = useState(1);
  const [items, setItems] = useState<VentaItem[]>([]);
  const [vendedorId, setVendedorId] = useState('V-001');

  const stockQuery = useStockProducto(codigoBuscado);
  const ventaMutation = useVenta();

  const producto = stockQuery.data;
  const hayItems = items.length > 0;
  const ventaExitosa = ventaMutation.data;

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
        },
      ];
    });
    setCantidad(1);
  };

  const quitarItem = (productoId: string) => {
    setItems((prev) => prev.filter((i) => i.productoId !== productoId));
  };

  const confirmarVenta = () => {
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

  const errorConfirmacion = ventaMutation.error
    ? normalizarErrorApi(ventaMutation.error)
    : null;

  return (
    <main className="min-h-screen bg-slate-50 p-6">
      <PageHeader
        title="Procesar Venta"
        subtitle="HU-01 — Consulta el stock del producto y confirma la venta"
        meta={{ label: 'Vendedor', value: vendedorId }}
      />

      <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
        {/* Columna izquierda: búsqueda + producto */}
        <section className="space-y-4">
          <StockSearchInput
            value={inputCodigo}
            onValueChange={setInputCodigo}
            onSearch={setCodigoBuscado}
            placeholder="Buscar producto por código..."
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

        {/* Columna derecha: resumen de la venta */}
        <aside className="space-y-4">
          <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="mb-2 text-base font-semibold text-slate-900">
              Resumen de venta
            </h2>

            {!hayItems ? (
              <p className="text-sm text-slate-500">
                Todavía no hay productos agregados.
              </p>
            ) : (
              <ul className="divide-y divide-slate-100">
                {items.map((item) => (
                  <VentaItemRow
                    key={item.productoId}
                    item={item}
                    onQuitar={() => quitarItem(item.productoId)}
                  />
                ))}
              </ul>
            )}

            {hayItems && (
              <>
                <div className="mt-4 border-t border-slate-200 pt-3">
                  <p className="flex items-center justify-between text-sm font-semibold text-slate-900">
                    <span>Total</span>
                    <span>
                      $
                      {items.reduce(
                        (acc, i) => acc + i.precio * i.cantidad,
                        0,
                      )}
                    </span>
                  </p>
                </div>

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
              </>
            )}

            <Button
              type="button"
              className="mt-4 w-full"
              disabled={!hayItems || ventaMutation.isPending}
              onClick={confirmarVenta}
            >
              {ventaMutation.isPending ? 'Procesando...' : 'Confirmar venta'}
            </Button>
          </div>

          {errorConfirmacion && (
            <Alert
              variant="error"
              title="No se pudo completar la venta"
              message={errorConfirmacion}
            />
          )}

          {ventaExitosa && (
            <TicketCard
              venta={ventaExitosa}
              onImprimir={imprimirTicket}
              onCerrar={cerrarTicket}
            />
          )}
        </aside>
      </div>
    </main>
  );
}