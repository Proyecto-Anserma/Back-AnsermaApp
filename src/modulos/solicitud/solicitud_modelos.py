from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, field_serializer
from datetime import date
from typing import Any, Optional, List

from src.modulos.tipo_solicitud.tipo_solicitud_modelos import TipoSolicitudBase
from src.modulos.ubicacion.ubicacion_modelos import Ubicacion
from src.modulos.estado_solicitud.estado_solicitud_modelos import EstadoSolicitudResponse



class SolicitudBase(BaseModel):
    id_solicitud: Optional[int] = None  # Campo opcional con valor por defecto None
    descripcion_solicitud: str
    fecha_creacion_solicitud: Optional[date] = date.today()
    id_tipo_solicitud: int
    id_ubicacion_solicitud: int
    id_ciudadano_solicitud: str
    foto_solicitud: Optional[str] = None
    cantidad_solicitud: int  # Nuevo campo

class SolicitudFiltrar(BaseModel):
    descripcion_solicitud: Optional[str] = None
    id_ciudadano_solicitud: Optional[str] = None
    cantidad_solicitud: Optional[int] = None

class SolicitudCreate(SolicitudBase):
    geolocalizacion: str

class SolicitudResponse(SolicitudBase):
    id_solicitud: int
    descripcion_solicitud: str
    fecha_creacion_solicitud: date
    foto_solicitud: Optional[str] = None
    geolocalizacion: Any
    id_tipo_solicitud: int
    id_ubicacion_solicitud: int
    id_ciudadano_solicitud: str
    tipo_solicitud: Optional[TipoSolicitudBase] = None
    ubicacion: Optional[Ubicacion] = None
    estados: List[EstadoSolicitudResponse] = [] 


    @field_serializer('geolocalizacion')
    def serialize_geometry(self, geom: Any) -> str:
        if isinstance(geom, WKBElement):
            return f"SRID=4326;{to_shape(geom).wkt}"
        return str(geom)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True