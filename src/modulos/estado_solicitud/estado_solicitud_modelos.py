from datetime import date
from pydantic import BaseModel, Field
from typing import Any, Optional

class EstadoBase(BaseModel):
    id_estado: int
    descripcion_estado: str

    class Config:
        from_attributes = True

class EstadoSolicitudBase(BaseModel):
    fecha_cambio_estado_solicitud: date
    observacion_solicitud: Optional[str] = Field(None, max_length=100)
    id_solicitud: int
    id_estado: int

class EstadoSolicitudCreate(EstadoSolicitudBase):
    pass

class EstadoSolicitudUpdate(BaseModel):
    fecha_cambio_estado_solicitud: Optional[date] = None
    observacion_solicitud: Optional[str] = Field(None, max_length=100)
    id_solicitud: Optional[int] = None
    id_estado: Optional[int] = None
    
class EstadoSolicitudResponse(EstadoSolicitudBase):
    id_estado_solicitud: int
    estado: Optional[EstadoBase] = None

    class Config:
        from_attributes = True

class EstadoSolicitudFiltro(BaseModel):
    id_solicitud: Optional[int] = None
