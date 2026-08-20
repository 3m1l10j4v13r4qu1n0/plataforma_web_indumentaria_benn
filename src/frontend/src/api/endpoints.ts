/**
 * ⚠️ LISTA OFICIAL DE ENDPOINTS DEL BACKEND
 * Solo se pueden consumir estos endpoints.
 * Si necesitas uno que no está aquí, DETÉN la implementación.
 * Verificado contra app/presentation/routers/venta_router.py.
 */
export const API_ENDPOINTS = {
  // Ventas
  VENTAS: {
    CREATE: '/api/v1/ventas',
  },

  // Productos
  PRODUCTOS: {
    STOCK: (codigo: string) => `/api/v1/productos/${codigo}/stock`,
  },
} as const;