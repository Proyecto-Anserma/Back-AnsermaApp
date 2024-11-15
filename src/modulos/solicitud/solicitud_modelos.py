from pydantic import BaseModel
from datetime import date
from typing import Optional

class SolicitudBase(BaseModel):
    descripcion_solicitud: str
    fecha_creacion_solicitud: date
    foto_solicitud: Optional[str] = None
    geolocalizacion: Optional[str] = None  # Guardaremos el punto geográfico como un string tipo WKT (Well Known Text)
    id_tipo_solicitud: int
    id_ubicacion_solicitud: int
    id_ciudadano_solicitud: int

class SolicitudCreate(SolicitudBase):
    pass

class SolicitudUpdate(SolicitudBase):
    descripcion_solicitud: Optional[str] = None
    fecha_creacion_solicitud: Optional[date] = None
