import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { ROUTES } from '@/constants/routes';
import { cn } from '@/utils/cn';

const NAV_LINKS = [
  { to: ROUTES.DASHBOARD, label: 'Dashboard' },
  { to: ROUTES.PRODUCTOS_STOCK, label: 'Consulta de Stock' },
  {to: ROUTES.VENTAS, label: 'Nueva Venta' },
  { to: ROUTES.CAMBIOS, label: 'Registrar Cambio' },
] as const;

/**
 * Barra de navegación superior fija.
 * Muestra links de navegación, info del usuario y botón de logout.
 *
 * SRP: Solo presenta navegación, sin lógica de negocio.
 */
export function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate(ROUTES.LOGIN, { replace: true });
  };

  return (
    <nav className="sticky top-0 z-50 border-b border-slate-200 bg-white shadow-sm">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 sm:px-6">
        {/* Logo + links */}
        <div className="flex items-center gap-6">
          <Link
            to={ROUTES.PRODUCTOS_STOCK}
            className="text-lg font-bold text-brand-700"
          >
            SGVIR
          </Link>

          <div className="hidden items-center gap-1 sm:flex">
            {NAV_LINKS.map((link) => {
              const isActive = location.pathname === link.to;
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  className={cn(
                    'rounded-md px-3 py-1.5 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-brand-50 text-brand-700'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900',
                  )}
                >
                  {link.label}
                </Link>
              );
            })}
          </div>
        </div>

        {/* Usuario + logout */}
        <div className="flex items-center gap-4">
          {user && (
            <div className="hidden text-right sm:block">
              <p className="text-sm font-medium text-slate-700">{user.nombre}</p>
              <p className="text-xs text-slate-400">{user.rol}</p>
            </div>
          )}
          <button
            type="button"
            onClick={handleLogout}
            className="rounded-md px-3 py-1.5 text-sm font-medium text-slate-500 transition-colors hover:bg-red-50 hover:text-red-600"
          >
            Cerrar sesión
          </button>
        </div>
      </div>

      {/* Menú móvil (links apilados) */}
      <div className="flex gap-1 border-t border-slate-100 px-4 py-2 sm:hidden">
        {NAV_LINKS.map((link) => {
          const isActive = location.pathname === link.to;
          return (
            <Link
              key={link.to}
              to={link.to}
              className={cn(
                'rounded-md px-3 py-1.5 text-xs font-medium transition-colors',
                isActive
                  ? 'bg-brand-50 text-brand-700'
                  : 'text-slate-500 hover:bg-slate-50',
              )}
            >
              {link.label}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
