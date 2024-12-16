from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from ..solicitud_ayuda.solicitud_ayuda_modelos import SolicitudAyudaResponse
from ..cantidad_origen_ayuda.cantidad_origen_ayuda_modelos import CantidadOrigenAyudaResponse

class AyudaBase(BaseModel):
    descripcion_solicitud: str
    fecha_creacion_ayuda: date
    observacion_ayuda: Optional[str] = None
    foto_solicitud: Optional[str] = None

class AyudaCreate(AyudaBase):
    pass

class AyudaResponse(AyudaBase):
    id_ayuda: int
    solicitudes_ayuda: List[SolicitudAyudaResponse] = []
    cantidades_origen_ayuda: List[CantidadOrigenAyudaResponse] = []

    class Config:
        from_attributes = True

class AyudasFiltrar(BaseModel):
    fecha_creacion_ayuda: Optional[date] = None