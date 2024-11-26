from pydantic import BaseModel, Field
from datetime import date
from typing import Any, Optional


class AyudaBase(BaseModel):
    descripcion_solicitud: str = Field(..., max_length=250)
    fecha_creacion_ayuda: date
    observacion_ayuda: str = Field(..., max_length=500)
    foto_solicitud: str

class AyudaCreate(AyudaBase):
    pass

class AyudaResponse(AyudaBase):
    id_ayuda: int

    class Config:
        orm_mode = True

class AyudasFiltrar(BaseModel):
    fecha_creacion_ayuda: Optional[date] = None