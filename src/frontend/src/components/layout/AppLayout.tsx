import { Outlet } from 'react-router-dom';
import { Navbar } from './Navbar';
import type { ReactNode } from 'react';

interface AppLayoutProps {
  children?: ReactNode;
}

/**
 * Layout compartido para todas las rutas autenticadas.
 * Renderiza el Navbar + el contenido (children o <Outlet>).
 */
export function AppLayout({ children }: AppLayoutProps) {
  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6">
        {children ?? <Outlet />}
      </div>
    </div>
  );
}
