from pydantic import BaseModel, Field
from datetime import date
from typing import Any, Optional, List
from src.modulos.cantidad_origen_ayuda.cantidad_origen_ayuda_modelos import CantidadOrigenAyudaResponse

class SolicitudAyudaEnAyuda(BaseModel):
    id_solicitud_ayuda: int
    cantidad_solicitud_ayuda: int
    fecha_entrega_solicitud_ayuda: date
    foto_entrega_solicitud_ayuda: str
    id_solicitud: int
    id_ayuda: int

    class Config:
        from_attributes = True

class AyudaBase(BaseModel):
    descripcion_solicitud: str = Field(..., max_length=250)
    fecha_creacion_ayuda: date
    observacion_ayuda: str = Field(..., max_length=500)
    foto_solicitud: str

class AyudaCreate(AyudaBase):
    pass

class AyudaResponse(AyudaBase):
    id_ayuda: int
    solicitudes_ayuda: List[SolicitudAyudaEnAyuda] = []
    cantidades_origen_ayuda: List[CantidadOrigenAyudaResponse] = []

    class Config:
        from_attributes = True

class AyudasFiltrar(BaseModel):
    fecha_creacion_ayuda: Optional[date] = None