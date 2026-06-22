import { Routes, Route, Navigate } from 'react-router-dom';
import { ConsultarStockPage } from '@/pages/productos/ConsultarStockPage';
import { NuevaVentaPage } from '@/pages/ventas/NuevaVentaPage';

/**
 * Router principal de la aplicación SGVIR.
 *
 * ⚠️ Nota sobre autenticación:
 * El backend AÚN no tiene endpoints de auth implementados.
 * Por YAGNI, NO envolvemos rutas en <ProtectedRoute /> todavía.
 */
export function AppRouter() {
  return (
    <Routes>
      {/* Redirección raíz → primera pantalla disponible */}
      <Route path="/" element={<Navigate to="/ventas/nueva" replace />} />

      {/* HU-01: Nueva Venta (pantalla principal) */}
      <Route path="/ventas/nueva" element={<NuevaVentaPage />} />

      {/* HU-06: Consultar stock disponible */}
      <Route path="/productos/stock" element={<ConsultarStockPage />} />

      {/* Placeholders para futuras HUs */}
      <Route path="/cambios" element={<Placeholder page="Cambios" />} />

      {/* Fallback 404 */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}

function Placeholder({ page }: { page: string }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50">
      <div className="rounded-lg border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="text-xl font-semibold text-slate-800">
          {page} — Próximamente
        </h1>
        <p className="mt-2 text-sm text-slate-500">
          Esta pantalla está en desarrollo.
        </p>
      </div>
    </div>
  );
}

function NotFoundPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-slate-800">404</h1>
        <p className="mt-2 text-slate-500">Ruta no encontrada</p>
        <a
          href="/ventas/nueva"
          className="mt-4 inline-block text-sm font-medium text-brand-600 hover:underline"
        >
          Volver a Nueva Venta
        </a>
      </div>
    </div>
  );
}
