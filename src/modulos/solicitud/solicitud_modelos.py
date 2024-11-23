from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, field_serializer
from datetime import date
from typing import Any, Optional

class SolicitudBase(BaseModel):
    descripcion_solicitud: str
    fecha_creacion_solicitud: date
    foto_solicitud: Optional[str] = None
    id_tipo_solicitud: int
    id_ubicacion_solicitud: int
    id_ciudadano_solicitud: str

class SolicitudFiltrar(BaseModel):
    descripcion_solicitud: Optional[str] = None
    id_ciudadano_solicitud: Optional[str] = None

class SolicitudCreate(SolicitudBase):
    geolocalizacion: str

class SolicitudResponse(SolicitudBase):
    geolocalizacion: Any

    @field_serializer('geolocalizacion')
    def serialize_geometry(self, geom: Any) -> str:
        if isinstance(geom, WKBElement):
            return f"SRID=4326;{to_shape(geom).wkt}"
        return str(geom)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True