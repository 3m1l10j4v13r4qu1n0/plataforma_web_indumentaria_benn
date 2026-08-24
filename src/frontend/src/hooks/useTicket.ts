import { useState, useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import { ventaService } from '@/api/services/venta.service';
import type { ValidarTicketResponse } from '@/types/api';
import { normalizarErrorApi } from '@/utils/apiErrors';

interface UseTicketResult {
  /** Número de ticket ingresado por el cajero */
  numeroTicket: string;
  /** Actualizar el número de ticket (no dispara la búsqueda) */
  setNumeroTicket: (value: string) => void;
  /** Disparar la búsqueda del ticket con el valor actual */
  buscarTicket: () => void;
  /** Datos de la compra original si el ticket es válido */
  compra: ValidarTicketResponse | null;
  /** Está cargando la búsqueda */
  isLoading: boolean;
  /** Error amigable de la búsqueda (ej. TICKET_NO_ENCONTRADO) */
  error: string | null;
  /** Indica si se realizó al menos una búsqueda */
  buscoAlMenosUnaVez: boolean;
  /** Limpia la búsqueda para iniciar otro cambio */
  reiniciar: () => void;
}

/**
 * Hook que encapsula la búsqueda de un ticket de compra (HU-04).
 *
 * La búsqueda solo se dispara cuando el usuario confirma (Enter o botón).
 * El error se normaliza con `normalizarErrorApi` para traducir códigos del
 * backend (ej. TICKET_NO_ENCONTRADO) a mensajes amigables.
 *
 * SRP: Maneja estado de búsqueda + llamada al servicio.
 */
export function useTicket(): UseTicketResult {
  const [inputValue, setInputValue] = useState('');
  const [activeTicket, setActiveTicket] = useState('');
  const [buscoAlMenosUnaVez, setBuscoAlMenosUnaVez] = useState(false);

  const buscarTicket = useCallback(() => {
    const trimmed = inputValue.trim();
    if (!trimmed) return;
    setActiveTicket(trimmed);
    setBuscoAlMenosUnaVez(true);
  }, [inputValue]);

  const reiniciar = useCallback(() => {
    setInputValue('');
    setActiveTicket('');
    setBuscoAlMenosUnaVez(false);
  }, []);

  const { data, isPending, error } = useQuery({
    queryKey: ['validar-ticket', activeTicket],
    queryFn: () => ventaService.validarTicket(activeTicket),
    enabled: activeTicket.length > 0,
    retry: false,
  });

  return {
    numeroTicket: inputValue,
    setNumeroTicket: setInputValue,
    buscarTicket,
    compra: data ?? null,
    isLoading: isPending,
    error: error ? normalizarErrorApi(error) : null,
    buscoAlMenosUnaVez,
    reiniciar,
  };
}
