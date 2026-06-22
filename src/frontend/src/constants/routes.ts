/*/**
 * Rutas internas del frontend.
 * Centralizadas para evitar strings mágicos en <Link to="..."> y navigate().
 */
export const ROUTES = {
  HOME: '/',
  PRODUCTOS_STOCK: '/productos/stock',
  VENTAS_NUEVA: '/ventas/nueva',
  VENTAS: '/ventas',
  CAMBIOS: '/cambios',
  LOGIN: '/login', // Preparado para fase futura de auth (YAGNI)
} as const;

export type RoutePath = (typeof ROUTES)[keyof typeof ROUTES];
