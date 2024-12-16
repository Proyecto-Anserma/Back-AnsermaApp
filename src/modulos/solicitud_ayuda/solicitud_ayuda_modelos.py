from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class SolicitudAyudaBase(BaseModel):
    cantidad_solicitud_ayuda: int = Field(..., description="Cantidad de la ayuda solicitada")
    id_solicitud: int = Field(..., description="ID de la solicitud relacionada")
    id_ayuda: int = Field(..., description="ID de la ayuda relacionada")

class SolicitudAyudaCreate(SolicitudAyudaBase):
    fecha_entrega_solicitud_ayuda: Optional[date] = None
    foto_entrega_solicitud_ayuda: Optional[str] = None

class SolicitudAyudaResponse(BaseModel):
    id_solicitud_ayuda: int
    cantidad_solicitud_ayuda: int
    fecha_entrega_solicitud_ayuda: Optional[date] = None
    foto_entrega_solicitud_ayuda: Optional[str] = None
    id_solicitud: int
    id_ayuda: int

    class Config:
        from_attributes = True
