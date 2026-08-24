import { Routes, Route, Navigate } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';
import { ConsultarStockPage } from '@/pages/productos/ConsultarStockPage';
import { CrearVentaPage } from '@/pages/ventas/CrearVentaPage';
import { RegistrarCambioPage } from '@/pages/cambios/RegistrarCambioPage';

/**
 * Router principal de la aplicación SGVIR.
 *
 * ⚠️ Nota sobre autenticación:
 * El backend AÚN no tiene endpoints de auth implementados.
 * Por YAGNI, NO envolvemos rutas en <ProtectedRoute /> todavía.
 * Cuando el backend exponga /auth/login, se activará la protección aquí.
 */
export function AppRouter() {
  return (
    <Routes>
      {/* Redirección raíz → primera pantalla disponible */}
      <Route path="/" element={<Navigate to={ROUTES.PRODUCTOS_STOCK} replace />} />

      {/* HU-06: Consultar stock disponible */}
      <Route path="/productos/stock" element={<ConsultarStockPage />} />

      {/* HU-01: Procesar venta (validar stock antes de vender) */}
      <Route path="/ventas" element={<CrearVentaPage />} />

      {/* HU-04 + HU-02 + HU-03: Flujo de cambios de productos */}
      <Route path={ROUTES.CAMBIOS} element={<RegistrarCambioPage />} />

      {/* Fallback 404 */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}

function NotFoundPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-slate-800">404</h1>
        <p className="mt-2 text-slate-500">Ruta no encontrada</p>
        <a
          href="/productos/stock"
          className="mt-4 inline-block text-sm font-medium text-brand-600 hover:underline"
        >
          Volver a Consultar Stock
        </a>
      </div>
    </div>
  );
}