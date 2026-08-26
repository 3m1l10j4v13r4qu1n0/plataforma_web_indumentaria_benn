import { Routes, Route, Navigate, Link } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';
import { ProtectedRoute } from '@/routes/ProtectedRoute';
import { AppLayout } from '@/components/layout/AppLayout';
import { LoginPage } from '@/pages/auth/LoginPage';
import { RegisterPage } from '@/pages/auth/RegisterPage';
import { DashboardPage } from '@/pages/dashboard/DashboardPage';
import { ConsultarStockPage } from '@/pages/productos/ConsultarStockPage';
import { CrearVentaPage } from '@/pages/ventas/CrearVentaPage';
import { RegistrarCambioPage } from '@/pages/cambios/RegistrarCambioPage';

/**
 * Router principal de la aplicación SGVIR.
 * Todas las rutas de negocio requieren autenticación (ProtectedRoute)
 * y se renderizan dentro de AppLayout (navbar + contenido).
 */
export function AppRouter() {
  return (
    <Routes>
      {/* Login — ruta pública, sin layout */}
      <Route path={ROUTES.LOGIN} element={<LoginPage />} />

      {/* Home redirige al dashboard */}
      <Route
        path={ROUTES.HOME}
        element={
          <ProtectedRoute>
            <Navigate to={ROUTES.DASHBOARD} replace />
          </ProtectedRoute>
        }
      />

      {/* Registro — solo GERENTE */}
      <Route
        path={ROUTES.REGISTRO}
        element={
          <ProtectedRoute allowedRoles={['GERENTE']}>
            <AppLayout>
              <RegisterPage />
            </AppLayout>
          </ProtectedRoute>
        }
      />

      {/* Rutas protegidas — dentro de AppLayout (navbar) */}
      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path={ROUTES.DASHBOARD} element={<DashboardPage />} />
        <Route path={ROUTES.PRODUCTOS_STOCK} element={<ConsultarStockPage />} />
        <Route path={ROUTES.VENTAS} element={<CrearVentaPage />} />
        <Route path={ROUTES.CAMBIOS} element={<RegistrarCambioPage />} />
      </Route>

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
        <Link
          to={ROUTES.DASHBOARD}
          className="mt-4 inline-block text-sm font-medium text-brand-600 hover:underline"
        >
          Volver al Dashboard
        </Link>
      </div>
    </div>
  );
}
