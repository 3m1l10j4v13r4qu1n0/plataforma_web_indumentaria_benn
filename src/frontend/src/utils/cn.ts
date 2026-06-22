import { clsx, type ClassValue } from 'clsx';
import 'tailwind-merge';
import { twMerge } from 'tailwind-merge';

/**
 * Utilidad para combinar clases de Tailwind de forma segura.
 * DRY: Centralizada para evitar duplicación en cada componente.
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
