export interface RegistroRequest {
  email: string;
  password: string;
  nombre: string;
  rol: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface RefreshRequest {
  refresh_token: string;
}

export interface UsuarioResponse {
  id: string;
  email: string;
  nombre: string;
  rol: string;
  activo: boolean;
}
