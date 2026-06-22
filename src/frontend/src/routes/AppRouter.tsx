import { Routes, Route, Navigate } from 'react-router-dom';

export function AppRouter() {
  return (
    <Routes>
      {/* Ruta raíz temporal — se reemplazará en el Paso 2 */}
      <Route path="/" element={<Navigate to="/ventas" replace />} />

      {/* Placeholder de rutas — se completarán en el Paso 2 */}
      <Route path="/ventas" element={<div>Pantalla de Ventas (próximamente)</div>} />
      <Route path="/productos" element={<div>Consulta de Stock (próximamente)</div>} />
      <Route path="/cambios" element={<div>Gestión de Cambios (próximamente)</div>} />

      {/* Fallback */}
      <Route path="*" element={<div>404 — Ruta no encontrada</div>} />
    </Routes>
  );
}