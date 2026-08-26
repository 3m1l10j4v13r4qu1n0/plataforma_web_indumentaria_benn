/**
 * Rutas internas del frontend.
 * Centralizadas para evitar strings mágicos en <Link to="..."> y navigate().
 */
export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  PRODUCTOS_STOCK: '/productos/stock',
  VENTAS: '/ventas',
  CAMBIOS: '/cambios',
  LOGIN: '/login',
  REGISTRO: '/registro',
} as const;

export type RoutePath = (typeof ROUTES)[keyof typeof ROUTES];