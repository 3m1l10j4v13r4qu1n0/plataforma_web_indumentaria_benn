/**
 * ⚠️ LISTA OFICIAL DE ENDPOINTS DEL BACKEND
 * Solo se pueden consumir estos endpoints.
 * Si necesitas uno que no está aquí, DETÉN la implementación.
 * Verificado contra app/presentation/routers/.
 */
export const API_ENDPOINTS = {
  // Ventas
  VENTAS: {
    CREATE: '/api/v1/ventas',
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
} as const;