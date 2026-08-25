import { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { authService } from '@/api/services/auth.service';
import { ROUTES } from '@/constants/routes';
import type { FormEvent } from 'react';

export function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = (location.state as { from?: { pathname: string } })?.from?.pathname
    ?? ROUTES.PRODUCTOS_STOCK;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const tokenResponse = await authService.login({ email, password });

      // Decodificar el payload del access token para obtener usuario
      const payload = JSON.parse(
        atob(tokenResponse.access_token.split('.')[1]),
      );

      login(
        {
          id: payload.sub,
          nombre: payload.sub,
          rol: payload.rol,
        },
        tokenResponse.access_token,
      );

      // Persistir refresh token
      localStorage.setItem('auth_refresh_token', tokenResponse.refresh_token);

      navigate(from, { replace: true });
    } catch (err: unknown) {
      const apiErr = err as { response?: { data?: { mensaje?: string } } };
      setError(
        apiErr.response?.data?.mensaje
        ?? 'Credenciales inválidas. Intente nuevamente.',
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4">
      <div className="w-full max-w-sm">
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-bold text-slate-800">SGVIR</h1>
          <p className="mt-1 text-sm text-slate-500">
            Plataforma Web Indumentaria BENN
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm"
        >
          <h2 className="mb-4 text-lg font-semibold text-slate-700">
            Iniciar sesión
          </h2>

          {error && (
            <div className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-700">
              {error}
            </div>
          )}

          <div className="mb-4">
            <label
              htmlFor="email"
              className="mb-1 block text-sm font-medium text-slate-600"
            >
              Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-800 placeholder-slate-400 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
              placeholder="usuario@benn.com"
            />
          </div>

          <div className="mb-6">
            <label
              htmlFor="password"
              className="mb-1 block text-sm font-medium text-slate-600"
            >
              Contraseña
            </label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-800 placeholder-slate-400 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
              placeholder="••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 disabled:opacity-50"
          >
            {loading ? 'Ingresando...' : 'Ingresar'}
          </button>
        </form>

        <p className="mt-4 text-center text-xs text-slate-400">
          <Link
            to={ROUTES.PRODUCTOS_STOCK}
            className="text-brand-600 hover:underline"
          >
            Continuar sin sesión
          </Link>
        </p>
      </div>
    </div>
  );
}
