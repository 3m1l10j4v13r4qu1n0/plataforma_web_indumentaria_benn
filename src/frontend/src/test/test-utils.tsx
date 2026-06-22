import { render, type RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import type { ReactElement } from 'react';

/**
 * Crea un QueryClient fresco para cada test.
 * SRP: Evita fugas de cache entre pruebas.
 */
export function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false, // Tests rápidos, sin reintentos
        gcTime: 0,
      },
      mutations: {
        retry: false,
      },
    },
  });
}

interface WrapperProps {
  children: React.ReactNode;
}

/**
 * Wrapper que provee todos los contextos necesarios para tests.
 * DRY: Reutilizable en todas las pruebas de componentes/hooks.
 */
export function AllProviders({ children }: WrapperProps) {
  const queryClient = createTestQueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{children}</BrowserRouter>
    </QueryClientProvider>
  );
}

/**
 * Custom render que incluye los providers necesarios.
 * KISS: Mismo API que `render` de RTL, pero con providers inyectados.
 */
export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>,
) {
  return render(ui, { wrapper: AllProviders, ...options });
}

// Re-exportar todo de RTL para uso directo
export * from '@testing-library/react';
export { default as userEvent } from '@testing-library/user-event';