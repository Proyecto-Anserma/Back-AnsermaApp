from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class SolicitudAyudaBase(BaseModel):
    cantidad_solicitud_ayuda: int = Field(..., description="Cantidad de la ayuda solicitada")
    fecha_entrega_solicitud_ayuda: date = Field(..., description="Fecha de entrega de la ayuda")
    foto_entrega_solicitud_ayuda: str = Field(..., description="URL o ruta de la foto de entrega")
    id_solicitud: int = Field(..., description="ID de la solicitud relacionada")
    id_ayuda: int = Field(..., description="ID de la ayuda relacionada")

class SolicitudAyudaCreate(BaseModel):
    cantidad_solicitud_ayuda: int
    fecha_entrega_solicitud_ayuda: date
    foto_entrega_solicitud_ayuda: str
    id_solicitud: int
    id_ayuda: int

class SolicitudAyudaResponse(BaseModel):
    id_solicitud_ayuda: int
    cantidad_solicitud_ayuda: int
    fecha_entrega_solicitud_ayuda: date
    foto_entrega_solicitud_ayuda: str
    id_solicitud: int
    id_ayuda: int

    class Config:
        orm_mode = True
