from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional


class UsuarioBase(BaseModel):
    numero_identificacion_usuario: str = Field(..., max_length=50)
    nombre_usuario: str = Field(..., max_length=100)
    apellido_usuario: str = Field(..., max_length=100)
    fecha_nacimiento_usuario: date
    correo_electronico_usuario: Optional[EmailStr] = None
    telefono_usuario: int = Field(..., ge=0)
    id_genero_usuario: int
    id_pertenencia_etnica_usuario: int
    id_ubicacion_usuario: int
    id_rol_usuario: int


class UsuarioCreate(UsuarioBase):
    """Modelo para crear un usuario."""
    pass  


class UsuarioUpdate(BaseModel):
    """Modelo para actualizar un usuario (todos los campos opcionales)."""
    numero_identificacion_usuario: str = Field(..., max_length=50)
    nombre_usuario: Optional[str] = Field(None, max_length=100)
    apellido_usuario: Optional[str] = Field(None, max_length=100)
    fecha_nacimiento_usuario: Optional[date]
    correo_electronico_usuario: Optional[EmailStr] = None
    telefono_usuario: Optional[int] = Field(None, ge=0)
    id_genero_usuario: Optional[int]
    id_pertenencia_etnica_usuario: Optional[int]
    id_ubicacion_usuario: Optional[int]
    id_rol_usuario: Optional[int]


class UsuarioResponse(UsuarioBase):
    """Modelo para la respuesta de un usuario (añadir campos relacionados si es necesario)."""
    ubicacion: Optional[str] = None
    pertenencia_etnica: Optional[str] = None
    genero: Optional[str] = None
    rol: Optional[str] = None

    class Config:
        orm_mode = True
