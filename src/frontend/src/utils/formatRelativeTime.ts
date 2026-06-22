import { formatDistanceToNow } from 'date-fns';
import { es } from 'date-fns/locale';

/**
 * Formatea una fecha ISO a un texto relativo en español.
 *
 * Ejemplos:
 * - "hace 2 minutos"
 * - "hace 1 hora"
 * - "hace 3 días"
 *
 * SRP: Única responsabilidad — formateo de fechas relativas.
 * Pure function: misma entrada → misma salida, sin efectos secundarios.
 *
 * @param isoString - Fecha en formato ISO 8601
 * @returns Texto relativo en español
 */
export function formatRelativeTime(isoString: string): string {
  try {
    const date = new Date(isoString);
    if (Number.isNaN(date.getTime())) {
      return 'fecha desconocida';
    }
    return formatDistanceToNow(date, { addSuffix: true, locale: es });
  } catch {
    return 'fecha desconocida';
  }
}