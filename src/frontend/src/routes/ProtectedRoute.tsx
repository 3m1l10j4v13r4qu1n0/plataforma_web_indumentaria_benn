import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { ROUTES } from '@/constants/routes';
import type { ReactElement } from 'react';

interface ProtectedRouteProps {
  children: ReactElement;
  /** Si se provee, solo usuarios con uno de estos roles pueden acceder. */
  allowedRoles?: readonly string[];
}

export function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const { isAuthenticated, user } = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to={ROUTES.LOGIN} state={{ from: location }} replace />;
  }

  if (allowedRoles && user && !allowedRoles.includes(user.rol)) {
    return <Navigate to={ROUTES.PRODUCTOS_STOCK} replace />;
  }

  return children;
}
