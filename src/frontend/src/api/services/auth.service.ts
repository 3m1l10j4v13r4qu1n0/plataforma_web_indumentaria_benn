import { apiClient } from '@/api/client';
import { API_ENDPOINTS } from '@/api/endpoints';
import type {
  LoginRequest,
  RegistroRequest,
  TokenResponse,
  UsuarioResponse,
} from '@/types/api/auth.types';

export const authService = {
  async registro(data: RegistroRequest): Promise<UsuarioResponse> {
    const response = await apiClient.post<UsuarioResponse>(
      API_ENDPOINTS.AUTH.REGISTRO,
      data,
    );
    return response.data;
  },

  async login(data: LoginRequest): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>(
      API_ENDPOINTS.AUTH.LOGIN,
      data,
    );
    return response.data;
  },

  async refresh(refreshToken: string): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>(
      API_ENDPOINTS.AUTH.REFRESH,
      { refresh_token: refreshToken },
    );
    return response.data;
  },
};
