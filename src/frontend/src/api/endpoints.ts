/**
 * ⚠️ LISTA OFICIAL DE ENDPOINTS DEL BACKEND
 * Solo se pueden consumir estos endpoints.
 * Si necesitas uno que no está aquí, DETÉN la implementación.
 */
export const API_ENDPOINTS = {
  // Ventas
  VENTAS: {
    CREATE: '/api/v1/ventas',
    TICKET: (numeroTicket: string) => `/api/v1/ventas/tickets/${numeroTicket}`,
  },

  // Productos
  PRODUCTOS: {
    STOCK: (codigo: string) => `/api/v1/productos/${codigo}/stock`,
    BUSCAR: '/api/v1/productos/buscar',
  },

  // Cambios
  CAMBIOS: {
    VALIDAR_ELEGIBILIDAD: '/api/v1/cambios/validar-elegibilidad',
  },

  // Health
  HEALTH: '/health',
} as const;