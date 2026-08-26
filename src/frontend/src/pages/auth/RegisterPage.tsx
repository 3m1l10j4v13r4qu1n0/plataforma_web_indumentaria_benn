import { useState } from 'react';
import { Link } from 'react-router-dom';
import { authService } from '@/api/services/auth.service';
import { ROUTES } from '@/constants/routes';
import type { FormEvent } from 'react';

const ROLES = [
  { value: 'VENDEDOR', label: 'Vendedor' },
  { value: 'CAJERO', label: 'Cajero' },
  { value: 'GERENTE', label: 'Gerente' },
  { value: 'ENCARGADO_VENTAS', label: 'Encargado de Ventas' },
] as const;

export function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [nombre, setNombre] = useState('');
  const [rol, setRol] = useState('VENDEDOR');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);
    setLoading(true);

    try {
      await authService.registro({ email, password, nombre, rol });
      setSuccess(true);
      setEmail('');
      setPassword('');
      setNombre('');
      setRol('VENDEDOR');
    } catch (err: unknown) {
      const apiErr = err as { response?: { data?: { mensaje?: string } } };
      setError(
        apiErr.response?.data?.mensaje
        ?? 'Error al registrar usuario. Intente nuevamente.',
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-sm">
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-bold text-slate-800">SGVIR</h1>
          <p className="mt-1 text-sm text-slate-500">
            Registrar nuevo usuario
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm"
        >
          <h2 className="mb-4 text-lg font-semibold text-slate-700">
            Alta de usuario
          </h2>

          {error && (
            <div className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-700">
              {error}
            </div>
          )}

          {success && (
            <div className="mb-4 rounded-md bg-green-50 p-3 text-sm text-green-700">
              Usuario registrado exitosamente.
            </div>
          )}

          <div className="mb-4">
            <label
              htmlFor="nombre"
              className="mb-1 block text-sm font-medium text-slate-600"
            >
              Nombre
            </label>
            <input
              id="nombre"
              type="text"
              required
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-800 placeholder-slate-400 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
              placeholder="Nombre completo"
            />
          </div>

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

          <div className="mb-4">
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
              minLength={6}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-800 placeholder-slate-400 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
              placeholder="Min. 6 caracteres"
            />
          </div>

          <div className="mb-6">
            <label
              htmlFor="rol"
              className="mb-1 block text-sm font-medium text-slate-600"
            >
              Rol
            </label>
            <select
              id="rol"
              value={rol}
              onChange={(e) => setRol(e.target.value)}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-800 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            >
              {ROLES.map((r) => (
                <option key={r.value} value={r.value}>
                  {r.label}
                </option>
              ))}
            </select>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 disabled:opacity-50"
          >
            {loading ? 'Registrando...' : 'Registrar usuario'}
          </button>
        </form>

        <p className="mt-4 text-center text-xs text-slate-400">
          <Link
            to={ROUTES.PRODUCTOS_STOCK}
            className="text-brand-600 hover:underline"
          >
            Volver al inicio
          </Link>
        </p>
      </div>
    </div>
  );
}
