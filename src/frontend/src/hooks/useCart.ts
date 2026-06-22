import { useState, useCallback, useMemo } from 'react';
import type { ItemCarrito } from '@/types/domain';
import type { ProductoBusquedaItem } from '@/types/api';

interface UseCartResult {
  /** Lista de productos en el carrito */
  items: ItemCarrito[];
  /** Total de artículos (suma de cantidades) */
  totalArticulos: number;
  /** Total a pagar (suma de subtotales) */
  totalPagar: number;
  /** Agrega un producto al carrito (o incrementa si ya existe) */
  addProduct: (producto: ProductoBusquedaItem) => void;
  /** Remueve un producto del carrito */
  removeProduct: (productoId: string) => void;
  /** Actualiza la cantidad de un producto */
  updateQuantity: (productoId: string, cantidad: number) => void;
  /** Limpia el carrito */
  clearCart: () => void;
  /** Si el carrito está vacío */
  isEmpty: boolean;
}

/**
 * Hook que maneja el estado local del carrito de ventas.
 *
 * 🎯 Responsabilidades (SRP):
 * - Agregar productos al carrito
 * - Actualizar cantidades
 * - Remover productos
 * - Calcular totales
 *
 * ❌ NO hace:
 * - Llamadas HTTP (delegado a useProcessSale)
 * - Validación de stock (delegado a useCartValidation)
 * - Persistencia (solo estado en memoria)
 */
export function useCart(): UseCartResult {
  const [items, setItems] = useState<ItemCarrito[]>([]);

  const addProduct = useCallback((producto: ProductoBusquedaItem) => {
    setItems((prev) => {
      const existing = prev.find((item) => item.productoId === producto.producto_id);
      if (existing) {
        // Si ya existe, incrementa la cantidad (respetando stock)
        return prev.map((item) =>
          item.productoId === producto.producto_id
            ? { ...item, cantidad: Math.min(item.cantidad + 1, item.stockActual) }
            : item,
        );
      }
      // Si no existe, lo agrega con cantidad 1
      return [
        ...prev,
        {
          productoId: producto.producto_id,
          codigo: producto.codigo,
          nombre: producto.nombre,
          categoria: producto.categoria,
          precio: producto.precio,
          stockActual: producto.stock_actual,
          cantidad: 1,
        },
      ];
    });
  }, []);

  const removeProduct = useCallback((productoId: string) => {
    setItems((prev) => prev.filter((item) => item.productoId !== productoId));
  }, []);

  const updateQuantity = useCallback((productoId: string, cantidad: number) => {
    if (cantidad <= 0) {
      setItems((prev) => prev.filter((item) => item.productoId !== productoId));
      return;
    }
    setItems((prev) =>
      prev.map((item) =>
        item.productoId === productoId ? { ...item, cantidad } : item,
      ),
    );
  }, []);

  const clearCart = useCallback(() => {
    setItems([]);
  }, []);

  const totalArticulos = useMemo(
    () => items.reduce((sum, item) => sum + item.cantidad, 0),
    [items],
  );

  const totalPagar = useMemo(
    () => items.reduce((sum, item) => sum + item.precio * item.cantidad, 0),
    [items],
  );

  const isEmpty = items.length === 0;

  return {
    items,
    totalArticulos,
    totalPagar,
    addProduct,
    removeProduct,
    updateQuantity,
    clearCart,
    isEmpty,
  };
}
