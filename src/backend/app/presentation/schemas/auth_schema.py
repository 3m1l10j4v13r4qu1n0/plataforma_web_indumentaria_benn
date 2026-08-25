from pydantic import BaseModel, Field


class RegistroRequest(BaseModel):
    """Schema de entrada para el registro de un usuario nuevo."""

    email: str = Field(..., description="Email del usuario")
    password: str = Field(
        ..., min_length=6, description="Contraseña (mínimo 6 caracteres)"
    )
    nombre: str = Field(..., description="Nombre completo del usuario")
    rol: str = Field(..., description="Rol del usuario")


class LoginRequest(BaseModel):
    """Schema de entrada para el login."""

    email: str = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña")


class TokenResponse(BaseModel):
    """Schema de salida con los tokens de autenticación."""

    access_token: str = Field(..., description="Token de acceso JWT")
    refresh_token: str = Field(..., description="Token de refresco JWT")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="TTL del access token en segundos")


class RefreshRequest(BaseModel):
    """Schema de entrada para renovar el access token."""

    refresh_token: str = Field(..., description="Token de refresco JWT")


class UsuarioResponse(BaseModel):
    """Schema de salida con los datos del usuario registrado."""

    id: str = Field(..., description="ID único del usuario")
    email: str = Field(..., description="Email del usuario")
    nombre: str = Field(..., description="Nombre completo")
    rol: str = Field(..., description="Rol asignado")
    activo: bool = Field(..., description="Estado de la cuenta")
