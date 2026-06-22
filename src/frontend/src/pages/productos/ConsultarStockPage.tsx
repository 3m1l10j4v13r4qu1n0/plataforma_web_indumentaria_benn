import { useMemo } from 'react';
import { PageHeader } from '@/components/layout';
import {
  StockSearchInput,
  ResultsHeader,
  StockResultCard,
  EmptyState,
} from '@/components/ui';
import { useBuscarProductos } from '@/hooks/useBuscarProductos';
import { useStockSearch } from '@/hooks/useStockSearch';
import { formatRelativeTime } from '@/utils/formatRelativeTime';

/**
 * HU-06 — Consultar stock disponible.
 *
 * 🎯 Responsabilidades del contenedor (SRP):
 * - Orquestar hooks de estado y datos
 * - Manejar los 4 estados universales: idle, loading, error, success, empty
 * - Pasar props tipadas a componentes presentacionales
 *
 * ❌ NO hace:
 * - Llamadas HTTP directas (delegadas a useBuscarProductos)
 * - Lógica de presentación (delegada a componentes UI)
 * - Manejo de errores con try/catch (delegado al interceptor global)
 *
 * 📋 Mockup de referencia: docs/05_mockups/mockup_hu06.html
 */
export function ConsultarStockPage() {
  const { query, confirmedQuery, setQuery, confirmSearch } = useStockSearch();
  const { productos, total, isLoading, isFetching, error, hasSearched } =
    useBuscarProductos(confirmedQuery);

  // Fecha formateada para el header (memoizada para evitar re-renders)
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

  return (
    <main className="min-h-screen bg-slate-50 p-4 sm:p-6 lg:p-8">
      <div className="mx-auto max-w-5xl">
        {/* Header de página */}
        <PageHeader
          title="POS — Consultar Stock (HU-06)"
          subtitle="Consulta de Stock en Tiempo Real"
          meta={{
            label: 'Vendedor',
            // ⚠️ YAGNI: placeholder hasta que AuthContext tenga datos reales.
            // Cuando se implemente auth, reemplazar por useAuth().user.nombre
            value: 'Carlos Ruiz',
          }}
          timestamp={currentDate}
        />

        {/* Barra de búsqueda */}
        <section className="mb-6">
          <StockSearchInput
            value={query}
            onChange={setQuery}
            onSearch={confirmSearch}
            disabled={isLoading}
            placeholder="Buscar por nombre o código..."
            aria-label="Buscar producto por nombre o código"
          />
        </section>

        {/* Área de resultados */}
        <section aria-live="polite" aria-busy={isLoading}>
          {renderContent({
            hasSearched,
            isLoading,
            isFetching,
            error,
            productos,
            total,
            confirmedQuery,
          })}
        </section>
      </div>
    </main>
  );
}

// ============================================================================
// Sub-componente privado: renderizado condicional de estados
// SRP: encapsula la lógica de los 4 estados universales
// ============================================================================

interface RenderContentProps {
  hasSearched: boolean;
  isLoading: boolean;
  isFetching: boolean;
  error: Error | null;
  productos: ReturnType<typeof useBuscarProductos>['productos'];
  total: number;
  confirmedQuery: string;
}

/**
 * Renderiza el contenido según el estado actual de la búsqueda.
 *
 * 🎯 Estados manejados (en orden de prioridad):
 * 1. Idle: aún no se ha buscado
 * 2. Loading: primera carga de una búsqueda
 * 3. Error: fallo en la petición HTTP
 * 4. Empty: búsqueda exitosa pero sin resultados
 * 5. Success: lista de productos
 */
function renderContent({
  hasSearched,
  isLoading,
  isFetching,
  error,
  productos,
  total,
  confirmedQuery,
}: RenderContentProps) {
  // 1. Estado Idle: sin búsqueda aún
  if (!hasSearched) {
    return (
      <EmptyState
        title="Comienza tu búsqueda"
        description="Escribe el nombre o código de un producto y presiona Enter para consultar el stock disponible."
        icon={<SearchIcon />}
      />
    );
  }

  // 2. Estado Loading: primera carga
  if (isLoading) {
    return <LoadingState query={confirmedQuery} />;
  }

  // 3. Estado Error: fallo HTTP
  if (error) {
    return <ErrorState error={error} />;
  }

  // 4. Estado Empty: sin resultados
  if (productos.length === 0) {
    return (
      <EmptyState
        title="Sin resultados"
        description={`No se encontraron productos que coincidan con "${confirmedQuery}".`}
      />
    );
  }

  // 5. Estado Success: lista de productos
  return (
    <div className="space-y-4">
      <ResultsHeader count={total} />

      {/* Indicador sutil de refetch en segundo plano */}
      {isFetching && (
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <span className="h-2 w-2 animate-pulse rounded-full bg-brand-500" />
          Actualizando resultados...
        </div>
      )}

      <ul className="space-y-3" role="list">
        {productos.map((producto) => (
          <li key={producto.codigo}>
            <StockResultCard
              codigo={producto.codigo}
              nombre={producto.nombre}
              categoria={producto.categoria ?? 'Sin categoría'}
              stockActual={producto.stockActual}
              stockMinimo={producto.stockMinimo}
              updatedAt={producto.actualizadoEn ?? new Date().toISOString()}
              lastUpdateRelative={formatRelativeTime(
                producto.actualizadoEn ?? new Date().toISOString(),
              )}
            />
          </li>
        ))}
      </ul>
    </div>
  );
}

// ============================================================================
// Sub-componentes privados de estados
// SRP: cada uno representa un estado visual específico
// ============================================================================

function LoadingState({ query }: { query: string }) {
  return (
    <div
      className="flex flex-col items-center justify-center rounded-lg border border-slate-200 bg-white py-12"
      role="status"
      aria-label="Cargando resultados"
    >
      <div className="h-10 w-10 animate-spin rounded-full border-4 border-slate-200 border-t-brand-600" />
      <p className="mt-4 text-sm text-slate-600">
        Buscando productos para "{query}"...
      </p>
    </div>
  );
}

function ErrorState({ error }: { error: Error }) {
  return (
    <div
      className="rounded-lg border border-rose-200 bg-rose-50 p-6"
      role="alert"
    >
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-rose-100">
          <svg
            className="h-5 w-5 text-rose-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-rose-900">
            Error al consultar stock
          </h3>
          <p className="mt-1 text-sm text-rose-700">
            No pudimos completar la búsqueda. Por favor, intenta nuevamente en
            unos segundos.
          </p>
          <p className="mt-2 text-xs text-rose-600">
            Detalle técnico: {error.message}
          </p>
        </div>
      </div>
    </div>
  );
}

function SearchIcon() {
  return (
    <svg
      className="h-12 w-12 text-slate-300"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={1.5}
        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
      />
    </svg>
  );
}