import { useEffect, useState, useCallback } from 'react';
import { StockSearchInput } from '@/components/ui';
import { useProductSearch } from '@/hooks/useProductSearch';
import type { ProductoBusquedaItem } from '@/types/api';
import type { ItemCarrito } from '@/types/domain';

interface ProductSearchBarProps {
  /** Callback cuando se encuentra un producto y se debe agregar al carrito */
  onProductFound: (producto: ProductoBusquedaItem) => void;
  /** IDs de productos ya en el carrito (para evitar duplicados) */
  productosEnCarrito: string[];
  /** Si está deshabilitada (ej: mientras procesa venta) */
  disabled?: boolean;
}

/**
 * Barra de búsqueda de productos para HU-01.
 *
 * 🎯 Flujo (KISS):
 * - Usuario escribe y presiona Enter
 * - Si hay exactamente 1 resultado → agregar al carrito
 * - Si hay 0 resultados → mostrar mensaje "no encontrado"
 * - Si hay múltiples resultados → pedir más especificidad
 *
 * SRP: Solo maneja la búsqueda y el feedback inmediato.
 *      No sabe de carrito ni de ventas.
 */
export function ProductSearchBar({
  onProductFound,
  productosEnCarrito,
  disabled = false,
}: ProductSearchBarProps) {
  const [query, setQuery] = useState('');
  const [feedback, setFeedback] = useState<{
    type: 'success' | 'error' | 'warning';
    message: string;
  } | null>(null);

  const { producto, mensaje, isLoading, hasSearched } = useProductSearch(query);

  // Limpia el feedback después de 3 segundos
  useEffect(() => {
    if (!feedback) return;
    const timer = setTimeout(() => setFeedback(null), 3000);
    return () => clearTimeout(timer);
  }, [feedback]);

  // Cuando la búsqueda devuelve resultado, procesarlo
  useEffect(() => {
    if (!hasSearched || isLoading) return;

    if (producto) {
      // Verificar si ya está en el carrito
      if (productosEnCarrito.includes(producto.producto_id)) {
        setFeedback({
          type: 'warning',
          message: `"${producto.nombre}" ya está en el carrito. Ajusta la cantidad en la tabla.`,
        });
        setQuery('');
        return;
      }

      // Agregar al carrito
      onProductFound(producto);
      setFeedback({
        type: 'success',
        message: `"${producto.nombre}" agregado al carrito.`,
      });
      setQuery('');
    } else if (hasSearched && mensaje.toLowerCase().includes('no se encontraron')) {
      setFeedback({
        type: 'error',
        message: 'Producto no encontrado. Verifica el código o nombre.',
      });
    } else if (hasSearched) {
      // Múltiples resultados
      setFeedback({
        type: 'warning',
        message: 'Se encontraron múltiples productos. Sé más específico.',
      });
    }
  }, [producto, mensaje, isLoading, hasSearched, productosEnCarrito, onProductFound]);

  const handleSearch = useCallback((value: string) => {
    setQuery(value);
  }, []);

  return (
    <div className="space-y-2">
      <div className="relative">
        <StockSearchInput
          value={query}
          onChange={setQuery}
          onSearch={handleSearch}
          disabled={disabled || isLoading}
          placeholder="Buscar o escanear producto (código o nombre)..."
          aria-label="Buscar producto para agregar a la venta"
        />

        {/* Spinner de carga */}
        {isLoading && (
          <div className="absolute right-12 top-1/2 -translate-y-1/2">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-brand-500 border-t-transparent" />
          </div>
        )}
      </div>

      {/* Feedback visual */}
      {feedback && (
        <div
          role="status"
          aria-live="polite"
          className={`rounded-md px-3 py-2 text-sm ${
            feedback.type === 'success'
              ? 'bg-emerald-50 text-emerald-800'
              : feedback.type === 'error'
                ? 'bg-rose-50 text-rose-800'
                : 'bg-amber-50 text-amber-800'
          }`}
        >
          {feedback.message}
        </div>
      )}
    </div>
  );
}
