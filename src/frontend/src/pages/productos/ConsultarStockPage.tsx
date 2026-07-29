import { useState } from 'react';
import { productosService } from '@/api/services/productos.service';
import { StockSearchInput } from '@/components/ui/StockSearchInput';
import type { StockResponse } from '@/types/api/productos.types';

export function ConsultarStockPage() {
  const [query, setQuery] = useState('');
  const [resultados, setResultados] = useState<StockResponse[]>([]);
  const [mensaje, setMensaje] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (value: string) => {
    setIsLoading(true);
    setError('');
    setMensaje('');

    try {
      const response = await productosService.buscarStock(value);
      setResultados(response.productos);
      setMensaje(response.mensaje);
    } catch {
      setResultados([]);
      setError('No se pudo consultar el stock. Intente nuevamente.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 p-6">
      <header className="mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Consulta de Stock</h1>
        <p className="text-sm text-slate-500">
          HU-06 — Busca productos por nombre o código para ver su disponibilidad.
        </p>
      </header>

      <section className="mx-auto max-w-3xl rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <StockSearchInput
          value={query}
          onValueChange={setQuery}
          onSearch={handleSearch}
          placeholder="Buscar por nombre o código"
          disabled={isLoading}
        />

        {isLoading && <p className="mt-4 text-sm text-slate-500">Buscando...</p>}
        {error && <p className="mt-4 text-sm text-red-600">{error}</p>}
        {mensaje && <p className="mt-4 text-sm text-slate-600">{mensaje}</p>}

        <div className="mt-6 space-y-3">
          {resultados.map((producto) => (
            <article key={producto.producto_id} className="rounded-lg border border-slate-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="font-semibold text-slate-900">{producto.nombre}</h2>
                  <p className="text-sm text-slate-500">{producto.producto_id}</p>
                </div>
                <div className="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">
                  Stock: {producto.stock_actual}
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}