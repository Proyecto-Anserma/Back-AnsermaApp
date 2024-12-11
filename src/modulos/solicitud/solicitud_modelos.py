from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, field_serializer
from datetime import date
from typing import Any, Optional

from src.modulos.tipo_solicitud.tipo_solicitud_modelos import TipoSolicitudBase
from src.modulos.ubicacion.ubicacion_modelos import Ubicacion



class SolicitudBase(BaseModel):
    id_solicitud: Optional[int] = None  # Campo opcional con valor por defecto None
    descripcion_solicitud: str
    fecha_creacion_solicitud: Optional[date] = date.today()
    id_tipo_solicitud: int
    id_ubicacion_solicitud: int
    id_ciudadano_solicitud: str
    foto_solicitud: Optional[str] = None

class SolicitudFiltrar(BaseModel):
    descripcion_solicitud: Optional[str] = None
    id_ciudadano_solicitud: Optional[str] = None

class SolicitudCreate(SolicitudBase):
    geolocalizacion: str

class SolicitudResponse(SolicitudBase):
    geolocalizacion: Any
    tipo_solicitud: Optional[TipoSolicitudBase] = None
    ubicacion: Optional[Ubicacion] = None


    @field_serializer('geolocalizacion')
    def serialize_geometry(self, geom: Any) -> str:
        if isinstance(geom, WKBElement):
            return f"SRID=4326;{to_shape(geom).wkt}"
        return str(geom)

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True