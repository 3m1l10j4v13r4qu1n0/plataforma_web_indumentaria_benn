import { Routes, Route, Navigate } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';
import { ProtectedRoute } from '@/routes/ProtectedRoute';
import { LoginPage } from '@/pages/auth/LoginPage';
import { RegisterPage } from '@/pages/auth/RegisterPage';
import { ConsultarStockPage } from '@/pages/productos/ConsultarStockPage';
import { CrearVentaPage } from '@/pages/ventas/CrearVentaPage';
import { RegistrarCambioPage } from '@/pages/cambios/RegistrarCambioPage';

/**
 * Router principal de la aplicación SGVIR.
 * Todas las rutas de negocio requieren autenticación (ProtectedRoute).
 * Solo /login y / están disponibles sin sesión.
 */
export function AppRouter() {
  return (
    <Routes>
      {/* Login — ruta pública */}
      <Route path={ROUTES.LOGIN} element={<LoginPage />} />

      {/* Registro — ruta protegida (solo GERENTE, validado en el componente) */}
      <Route
        path={ROUTES.REGISTRO}
        element={
          <ProtectedRoute>
            <RegisterPage />
          </ProtectedRoute>
        }
      />

      {/* Rutas protegidas */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Navigate to={ROUTES.PRODUCTOS_STOCK} replace />
          </ProtectedRoute>
        }
      />
      <Route
        path="/productos/stock"
        element={
          <ProtectedRoute>
            <ConsultarStockPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/ventas"
        element={
          <ProtectedRoute>
            <CrearVentaPage />
          </ProtectedRoute>
        }
      />
      <Route
        path={ROUTES.CAMBIOS}
        element={
          <ProtectedRoute>
            <RegistrarCambioPage />
          </ProtectedRoute>
        }
      />

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