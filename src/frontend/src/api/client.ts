import axios from 'axios';
import type { ApiErrorResponse } from '@/types/api/error.types';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? '',
  timeout: 10_000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor de request: inyecta token si existe (preparación para auth futura)
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor de respuesta: manejo centralizado de errores HTTP
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isAxiosError(error) && error.response) {
      const apiError = error.response.data as ApiErrorResponse;
      // Aquí se podría disparar un evento global / notificación
      // Por ahora solo logueamos; el ErrorBoundary y los hooks manejarán el UX.
      console.error(
        `[API Error] ${error.response.status} - ${apiError?.error ?? 'UNKNOWN'}`,
      );
    }
    return Promise.reject(error);
  },
);