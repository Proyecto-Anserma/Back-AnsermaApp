from datetime import date
from pydantic import BaseModel
from typing import Any, Optional

class EstadoSolicitudBase(BaseModel):
    fecha_cambio_estado_solicitud: date
    id_solicitud: int
    id_estado: int
    

class EstadoSolicitudCreate(EstadoSolicitudBase):
    pass

class EstadoSolicitudUpdate(BaseModel):
    fecha_cambio_estado_solicitud: Optional[date] = None
    id_solicitud: Optional[int] = None
    id_estado: Optional[int] = None
    
class EstadoSolicitudResponse(EstadoSolicitudBase):
    id_estado_solicitud: int

    class Config:
        from_attributes = True
