import { useRef } from 'react';
import { useBuscarProductos } from '@/hooks/useBuscarProductos';
import {
  StockSearchInput,
  ResultsHeader,
  ProductoBusquedaCard,
  EmptyState,
  Alert,
} from '@/components/ui';

/**
 * HU-06 — Consultar stock disponible.
 *
 * Permite al vendedor buscar productos por nombre o código
 * y ver su stock actual en tiempo real.
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
  } = useBuscarProductos();

  const mostrarResultados = buscoAlMenosUnaVez && !isLoading && !error;
  const mostrarSinResultados =
    mostrarResultados && resultados.length === 0;

  return (
    <main className="min-h-screen bg-slate-50 p-6">
      <header className="mb-6">
        <h1 className="text-2xl font-bold text-slate-800">
          Consulta de Stock
        </h1>
        <p className="text-sm text-slate-500">
          Busca productos por nombre o código para ver su disponibilidad.
        </p>
      </header>

      <StockSearchInput
        ref={inputRef}
        value={query}
        onValueChange={setQuery}
        onSearch={ejecutarBusqueda}
        placeholder="Buscar por nombre o código (mínimo 3 caracteres)..."
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
            <ResultsHeader count={totalEncontrados} label="Productos encontrados" />
            <ul className="mt-4 space-y-3">
              {resultados.map((producto) => (
                <li key={producto.productoId}>
                  <ProductoBusquedaCard producto={producto} />
                </li>
              ))}
            </ul>
          </>
        )}

        {/* Sin resultados */}
        {mostrarSinResultados && (
          <EmptyState
            title="No se encontraron productos"
            description={
              mensajeBackend ||
              'Intenta buscar con otro nombre o código de producto.'
            }
          />
        )}
      </div>
    </main>
  );
}