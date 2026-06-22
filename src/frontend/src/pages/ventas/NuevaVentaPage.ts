import { useState, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { SaleHeader } from '@/components/layout';
import {
  CartTable,
  StockAlert,
  SaleSummary,
  SaleActionBar,
} from '@/components/ui';
import { ProductSearchBar } from '@/components/ventas/ProductSearchBar';
import { SaleTicketView } from '@/components/ventas/SaleTicketView';
import { useCart } from '@/hooks/useCart';
import { useCartValidation } from '@/hooks/useCartValidation';
import { useProcessSale } from '@/hooks/useProcessSale';
import { ROUTES } from '@/constants/routes';
import type { ProductoBusquedaItem } from '@/types/api';
import type { CartItemRowProps } from '@/components/ui/CartItemRow';

/**
 * ⚠️ YAGNI: Placeholder del vendedor hasta que AuthContext tenga datos reales.
 */
const VENDEDOR_ID_PLACEHOLDER = 'V-001';
const VENDEDOR_NOMBRE_PLACEHOLDER = 'Juan Pérez';
const CAJA_PLACEHOLDER = '01';

/**
 * HU-01 + HU-07 — Nueva Venta con Ticket Post-Venta.
 *
 * 🎯 Responsabilidades (SRP):
 * - Orquestar hooks de venta y validación
 * - Mostrar vista de ticket cuando la venta es exitosa
 * - Delegar simulación de impresión a SaleTicketView
 *
 * 📋 Flujo completo:
 * 1. Vendedor busca/agrega productos → Carrito
 * 2. Valida stock → Confirmar venta
 * 3. Backend procesa → Muestra SaleTicketView
 * 4. Simula impresión → Nueva venta
 */
export function NuevaVentaPage() {
  const navigate = useNavigate();

  // Hooks de estado y datos
  const {
    items,
    totalArticulos,
    totalPagar,
    addProduct,
    removeProduct,
    updateQuantity,
    clearCart,
    isEmpty,
  } = useCart();

  const { validacion, esProcesable } = useCartValidation(items);
  const { processSale, ventaProcesada, isProcessing, error, reset } = useProcessSale();

  // Estado local de UI
  const [showTicketView, setShowTicketView] = useState(false);

  // Snapshot del carrito al momento de procesar la venta (para el ticket)
  const [carritoSnapshot, setCarritoSnapshot] = useState(items);

  // Fecha formateada para el header
  const currentDate = useMemo(
    () =>
      new Date().toLocaleDateString('es-AR', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      }),
    [],
  );

  // IDs de productos en el carrito
  const productosEnCarrito = useMemo(
    () => items.map((item) => item.productoId),
    [items],
  );

  // =========================================================================
  // Handlers
  // =========================================================================

  const handleProductFound = useCallback(
    (producto: ProductoBusquedaItem) => {
      addProduct(producto);
    },
    [addProduct],
  );

  const handleConfirmSale = useCallback(() => {
    if (!esProcesable) return;
    // Guarda snapshot del carrito antes de procesar
    setCarritoSnapshot([...items]);
    processSale(items, VENDEDOR_ID_PLACEHOLDER);
  }, [esProcesable, items, processSale]);

  const handleCancelSale = useCallback(() => {
    if (items.length > 0 && !window.confirm('¿Seguro que deseas cancelar la venta?')) {
      return;
    }
    clearCart();
    navigate(ROUTES.VENTAS_NUEVA);
  }, [items.length, clearCart, navigate]);

  const handleNuevaVenta = useCallback(() => {
    // Limpia todo y vuelve al estado inicial
    clearCart();
    setCarritoSnapshot([]);
    setShowTicketView(false);
    reset();
  }, [clearCart, reset]);

  // =========================================================================
  // Efectos: mostrar vista de ticket cuando la venta se procesa
  // =========================================================================

  if (ventaProcesada && !showTicketView) {
    setShowTicketView(true);
  }

  // =========================================================================
  // Mapeo de items a props de CartItemRow (presentacional)
  // =========================================================================

  const cartItemsProps: CartItemRowProps[] = items.map((item) => {
    const errorItem = validacion.errores.find((e) => e.productoId === item.productoId);
    return {
      nombre: item.nombre,
      codigo: item.codigo,
      precio: item.precio,
      stockActual: item.stockActual,
      cantidad: item.cantidad,
      onQuantityChange: (cantidad) => updateQuantity(item.productoId, cantidad),
      onRemove: () => removeProduct(item.productoId),
      hasStockError: !!errorItem,
      disabled: isProcessing,
    };
  });

  // =========================================================================
  // Render: Vista de Ticket (post-venta)
  // =========================================================================

  if (showTicketView && ventaProcesada) {
    return (
      <main className="min-h-screen bg-slate-50 p-4 sm:p-6 lg:p-8">
        <div className="mx-auto max-w-3xl">
          <SaleHeader
            title="POS — Ticket de Venta (HU-07)"
            cajero={VENDEDOR_NOMBRE_PLACEHOLDER}
            caja={CAJA_PLACEHOLDER}
            fecha={currentDate}
          />

          <SaleTicketView
            carrito={carritoSnapshot}
            ventaProcesada={ventaProcesada}
            totalArticulos={totalArticulos}
            totalPagar={totalPagar}
            onNuevaVenta={handleNuevaVenta}
          />
        </div>
      </main>
    );
  }

  // =========================================================================
  // Render: Vista de Nueva Venta (HU-01)
  // =========================================================================

  return (
    <main className="min-h-screen bg-slate-50 p-4 sm:p-6 lg:p-8">
      <div className="mx-auto max-w-6xl">
        {/* Header */}
        <SaleHeader
          title="POS — Nueva Venta (HU-01)"
          cajero={VENDEDOR_NOMBRE_PLACEHOLDER}
          caja={CAJA_PLACEHOLDER}
          fecha={currentDate}
        />

        {/* Barra de búsqueda */}
        <section className="mb-6" aria-label="Búsqueda de productos">
          <ProductSearchBar
            onProductFound={handleProductFound}
            productosEnCarrito={productosEnCarrito}
            disabled={isProcessing}
          />
        </section>

        {/* Tabla de productos */}
        <section className="mb-6" aria-label="Productos a vender">
          <CartTable items={cartItemsProps} disabled={isProcessing} />
        </section>

        {/* Alerta de errores de stock */}
        {!esProcesable && validacion.errores.length > 0 && (
          <section className="mb-6" aria-label="Errores de validación">
            <StockAlert
              items={validacion.errores.map((e) => ({
                nombre: e.nombre,
                motivo: e.motivo === 'CANTIDAD_CERO' ? 'SIN_STOCK' : e.motivo,
                stockDisponible: items.find((i) => i.productoId === e.productoId)?.stockActual,
              }))}
            />
          </section>
        )}

        {/* Error del backend al procesar venta */}
        {error && (
          <section className="mb-6" aria-label="Error al procesar venta">
            <div
              className="rounded-lg border border-rose-200 bg-rose-50 p-4"
              role="alert"
            >
              <div className="flex items-start gap-3">
                <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-rose-100">
                  <svg
                    className="h-4 w-4 text-rose-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                    />
                  </svg>
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-rose-900">
                    No se puede procesar la venta
                  </h3>
                  <p className="mt-1 text-sm text-rose-700">{error.message}</p>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Resumen + Acciones */}
        {!isEmpty && (
          <section className="space-y-4" aria-label="Resumen de la venta">
            <SaleSummary totalArticulos={totalArticulos} totalPagar={totalPagar} />
            <SaleActionBar
              onCancel={handleCancelSale}
              onConfirm={handleConfirmSale}
              confirmDisabled={!esProcesable}
              isProcessing={isProcessing}
            />
          </section>
        )}
      </div>
    </main>
  );
}
