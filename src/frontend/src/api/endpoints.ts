export const API_ENDPOINTS = {
  VENTAS: {
    CREATE: '/api/v1/ventas',
    TICKET: (numeroTicket: string) => `/api/v1/ventas/tickets/${numeroTicket}`,
  },
  PRODUCTOS: {
    STOCK: (codigo: string) => `/api/v1/productos/${codigo}/stock`,
    BUSCAR: '/api/v1/productos/buscar',
  },
  CAMBIOS: {
    VALIDAR_ELEGIBILIDAD: '/api/v1/cambios/validar-elegibilidad',
  },
  HEALTH: '/health',
} as const;
