import axios from 'axios';
import type { ApiErrorResponse } from '@/types/api/error.types';

const MENSAJES_AMIGABLES: Record<string, string> = {
  STOCK_INSUFICIENTE: 'No hay stock suficiente para completar la venta.',
  PRODUCTO_NO_ENCONTRADO: 'El producto consultado no existe.',
  DESCUENTO_EXCEDE_LIMITE:
    'El descuento supera el límite permitido. Se requiere autorización de gerente.',
  DESCUENTO_SIN_AUTORIZACION:
    'El descuento requiere la autorización de un gerente.',
  DESCUENTO_INVALIDO: 'El porcentaje de descuento no es válido.',
  TICKET_NO_ENCONTRADO:
    'El número de ticket no existe en el sistema. Verificá el comprobante.',
  VENTA_NO_ENCONTRADA: 'La venta consultada no existe en el sistema.',
  VENTA_YA_EN_CAMBIO:
    'La venta ya está en proceso de cambio en otra caja. No podés retenerla.',
  PLAZO_VENCIDO:
    'Pasaron más de 15 días desde la compra. El cambio fue rechazado.',
  CAMBIO_NO_ENCONTRADO: 'El cambio solicitado no existe en el sistema.',
  PRODUCTO_NO_APTO:
    'El producto no cumple las condiciones para ser cambiado (debe estar nuevo y con etiqueta).',
  OBSERVACIONES_REQUERIDAS:
    'Las observaciones son obligatorias cuando el producto no es apto.',
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