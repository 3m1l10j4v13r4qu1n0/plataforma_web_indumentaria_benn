/**
 * ⚠️ LISTA OFICIAL DE ENDPOINTS DEL BACKEND
 * Solo se pueden consumir estos endpoints.
 * Si necesitas uno que no está aquí, DETÉN la implementación.
 * Verificado contra app/presentation/routers/.
 */
export const API_ENDPOINTS = {
  // Auth (HU-09)
  AUTH: {
    REGISTRO: '/api/v1/auth/registro',
    LOGIN: '/api/v1/auth/login',
    REFRESH: '/api/v1/auth/refresh',
  },

  // Ventas
  VENTAS: {
    CREATE: '/api/v1/ventas',
    VALIDAR_TICKET: (numeroTicket: string) =>
      `/api/v1/ventas/validar-ticket/${encodeURIComponent(numeroTicket)}`,
    MARCAR_EN_CAMBIO: (numeroTicket: string) =>
      `/api/v1/ventas/${encodeURIComponent(numeroTicket)}/estado`,
  },

  // Cambios (HU-02, HU-03)
  CAMBIOS: {
    CREATE: '/api/v1/cambios',
    VALIDAR_ESTADO: (cambioId: string) =>
      `/api/v1/cambios/${encodeURIComponent(cambioId)}/validar-estado`,
  },

  // Productos
  PRODUCTOS: {
    STOCK: (codigo: string) => `/api/v1/productos/${codigo}/stock`,
    BUSCAR: (query: string) => `/api/v1/productos/buscar?query=${encodeURIComponent(query)}`,
  },

  // Descuentos (HU-05)
  DESCUENTOS: {
    APPLY: '/api/v1/descuentos',
  },

  // Dashboard
  DASHBOARD: {
    RESUMEN: '/api/v1/dashboard/resumen',
    PRODUCTOS_STOCK_BAJO: '/api/v1/dashboard/productos-stock-bajo',
  },
} as const;