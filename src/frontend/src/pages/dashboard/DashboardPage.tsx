import { Link } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { useResumenDashboard, useProductosStockBajo } from '@/hooks/useDashboard';
import { ROUTES } from '@/constants/routes';
import { formatoMoneda } from '@/utils/format';
import { Alert } from '@/components/ui';

const ACCESOS_RAPIDOS = [
  { to: ROUTES.PRODUCTOS_STOCK, label: 'Consulta de Stock', description: 'Buscar productos y ver stock en tiempo real' },
  { to: ROUTES.VENTAS, label: 'Nueva Venta', description: 'Registrar una venta y generar ticket' },
  { to: ROUTES.CAMBIOS, label: 'Registrar Cambio', description: 'Procesar cambio de producto' },
] as const;

/**
 * Dashboard principal — página de inicio autenticada.
 * Muestra métricas resumidas y accesos rápidos a las funcionalidades.
 */
export function DashboardPage() {
  const { user } = useAuth();
  const resumen = useResumenDashboard();
  const stockBajo = useProductosStockBajo();

  return (
    <div className="space-y-8">
      {/* Bienvenida */}
      <header>
        <h1 className="text-2xl font-bold text-slate-800">
          Hola, {user?.nombre ?? 'Usuario'}
        </h1>
        <p className="text-sm text-slate-500">
          Panel de control — {user?.rol}
        </p>
      </header>

      {/* Métricas */}
      {resumen.isError && (
        <Alert
          variant="error"
          title="Error al cargar el resumen"
          message="No se pudieron obtener las métricas del dashboard."
        />
      )}

      <div className="grid gap-4 sm:grid-cols-3">
        <MetricCard
          label="Ventas hoy"
          value={resumen.data?.ventas_hoy.toString() ?? '—'}
          loading={resumen.isLoading}
        />
        <MetricCard
          label="Facturado hoy"
          value={resumen.data != null ? formatoMoneda(resumen.data.total_facturado_hoy) : '—'}
          loading={resumen.isLoading}
        />
        <MetricCard
          label="Stock bajo"
          value={resumen.data?.productos_stock_bajo.toString() ?? '—'}
          loading={resumen.isLoading}
          alert={Boolean(resumen.data && resumen.data.productos_stock_bajo > 0)}
        />
      </div>

      {/* Accesos rápidos */}
      <section>
        <h2 className="mb-3 text-sm font-bold uppercase tracking-wide text-slate-500">
          Accesos rápidos
        </h2>
        <div className="grid gap-4 sm:grid-cols-3">
          {ACCESOS_RAPIDOS.map((acceso) => (
            <Link
              key={acceso.to}
              to={acceso.to}
              className="group rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition-all hover:border-brand-300 hover:shadow-md"
            >
              <h3 className="text-sm font-semibold text-slate-800 group-hover:text-brand-700">
                {acceso.label}
              </h3>
              <p className="mt-1 text-xs text-slate-500">{acceso.description}</p>
            </Link>
          ))}
        </div>
      </section>

      {/* Productos con stock bajo */}
      {stockBajo.data && stockBajo.data.length > 0 && (
        <section>
          <h2 className="mb-3 text-sm font-bold uppercase tracking-wide text-slate-500">
            Productos con stock bajo
          </h2>
          <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
            <ul className="divide-y divide-slate-100">
              {stockBajo.data.map((p) => (
                <li
                  key={p.producto_id}
                  className="flex items-center justify-between px-5 py-3"
                >
                  <div>
                    <p className="text-sm font-medium text-slate-700">{p.nombre}</p>
                    <p className="text-xs text-slate-400">{p.codigo}</p>
                  </div>
                  <span className="rounded-full bg-red-50 px-2.5 py-0.5 text-xs font-semibold text-red-600">
                    {p.stock_actual} uds.
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}
    </div>
  );
}

function MetricCard({
  label,
  value,
  loading,
  alert,
}: {
  label: string;
  value: string;
  loading: boolean;
  alert?: boolean;
}) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
        {label}
      </p>
      {loading ? (
        <div className="mt-2 h-8 w-20 animate-pulse rounded bg-slate-100" />
      ) : (
        <p
          className={`mt-2 text-2xl font-bold ${
            alert ? 'text-red-600' : 'text-slate-800'
          }`}
        >
          {value}
        </p>
      )}
    </div>
  );
}
