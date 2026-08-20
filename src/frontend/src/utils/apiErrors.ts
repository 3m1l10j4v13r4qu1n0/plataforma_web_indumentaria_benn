import axios from 'axios';
import type { ApiErrorResponse } from '@/types/api/error.types';

const MENSAJES_AMIGABLES: Record<string, string> = {
  STOCK_INSUFICIENTE: 'No hay stock suficiente para completar la venta.',
  PRODUCTO_NO_ENCONTRADO: 'El producto consultado no existe.',
};

/**
 * Normaliza un error de Axios a un mensaje amigable para el usuario.
 * Si el error no viene del backend, devuelve un mensaje genérico.
 */
export function normalizarErrorApi(error: unknown): string {
  if (axios.isAxiosError<ApiErrorResponse>(error) && error.response?.data) {
    const { error: code, mensaje } = error.response.data;
    return MENSAJES_AMIGABLES[code] ?? mensaje;
  }

  return 'Ocurrió un error inesperado. Intentalo de nuevo.';
}