from pydantic import BaseModel, Field
from datetime import date

class SolicitudAyudaBase(BaseModel):
    cantidad_solicitud_ayuda: int
    fecha_entrega_solicitud_ayuda: date
    foto_entrega_solicitud_ayuda: str

class SolicitudAyudaCreate(SolicitudAyudaBase):
    id_solicitud: int
    id_ayuda: int

class SolicitudAyudaResponse(SolicitudAyudaBase):
    id_solicitud_ayuda: int
    id_solicitud: int
    id_ayuda: int

    class Config:
        orm_mode = True
