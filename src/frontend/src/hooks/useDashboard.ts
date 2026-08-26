import { useQuery } from '@tanstack/react-query';
import { dashboardService } from '@/api/services/dashboard.service';

export function useResumenDashboard() {
  return useQuery({
    queryKey: ['dashboard', 'resumen'],
    queryFn: dashboardService.obtenerResumen,
    staleTime: 30_000,
  });
}

export function useProductosStockBajo() {
  return useQuery({
    queryKey: ['dashboard', 'stock-bajo'],
    queryFn: dashboardService.obtenerProductosStockBajo,
    staleTime: 30_000,
  });
}
