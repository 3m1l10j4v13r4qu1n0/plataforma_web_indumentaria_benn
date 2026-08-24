import { useRef } from 'react';
import { useBuscarProductos } from '@/hooks/useBuscarProductos';
import {
  StockSearchInput,
  ResultsHeader,
  ProductoBusquedaCard,
  EmptyState,
  Alert,
} from '@/components/ui';
import { PageHeader } from '@/components/layout/PageHeader';
import { formatoFechaCorta } from '@/utils/format';

/**
 * HU-06 — Consultar stock disponible.
 *
 * Permite al vendedor buscar productos por nombre o código
 * y ver su stock actual en tiempo real.
 * Textos según contrato visual (docs/05_mockups/mockup_hu06.html).
 *
 * SRP: Orquesta hook + componentes presentacionales.
 */
export function ConsultarStockPage() {
  const inputRef = useRef<HTMLInputElement>(null);
  const {
    query,
    setQuery,
    ejecutarBusqueda,
    resultados,
    totalEncontrados,
    mensajeBackend,
    isLoading,
    error,
    buscoAlMenosUnaVez,
    queryBuscada,
  } = useBuscarProductos();

  const mostrarResultados = buscoAlMenosUnaVez && !isLoading && !error;
  const mostrarSinResultados =
    mostrarResultados && resultados.length === 0;

  return (
    <main className="min-h-screen bg-slate-50 p-6">
      <PageHeader
        title="Consulta de Stock en Tiempo Real"
        meta={{ label: 'Vendedor', value: 'V-001' }}
        timestamp={formatoFechaCorta(new Date())}
        timestampLabel="Sistema"
      />

      <StockSearchInput
        ref={inputRef}
        value={query}
        onValueChange={setQuery}
        onSearch={ejecutarBusqueda}
        placeholder="Escanear código o escribir nombre del producto..."
      />

      <div className="mt-6">
        {/* Estado de carga */}
        {isLoading && (
          <div className="flex items-center justify-center py-12">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-300 border-t-brand-600" />
            <span className="ml-3 text-sm text-slate-500">Buscando productos...</span>
          </div>
        )}

        {/* Error */}
        {error && (
          <Alert
            variant="error"
            title="Error al buscar"
            message={error}
          />
        )}

        {/* Resultados */}
        {mostrarResultados && resultados.length > 0 && (
          <>
            <ResultsHeader count={totalEncontrados} />
            <ul className="mt-4 space-y-3">
              {resultados.map((producto) => (
                <li key={producto.productoId}>
                  <ProductoBusquedaCard producto={producto} />
                </li>
              ))}
            </ul>
          </>
        )}

        {/* Sin resultados (estado alternativo E-06 del contrato) */}
        {mostrarSinResultados && (
          <EmptyState
            title="Producto no encontrado"
            description={
              mensajeBackend ||
              `No existe ningún producto activo con el código o nombre "${queryBuscada}". Verifique el código de barras o intente con otra palabra clave.`
            }
          />
        )}
      </div>
    </main>
  );
}