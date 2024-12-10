from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class OrigenAyudaBase(BaseModel):
    nombre_entidad_origen_ayuda: str = Field(..., max_length=100)
    nit: str = Field(..., max_length=50)
    telefono_origen_ayuda: int
    correo_electronico_origen_ayuda: EmailStr
    zona_territorial_origen_ayuda: str = Field(..., max_length=100)

class OrigenAyudaCreate(OrigenAyudaBase):
    pass

class OrigenAyudaResponse(OrigenAyudaBase):
    id_origen_ayuda: int

    class Config:
        orm_mode = True
