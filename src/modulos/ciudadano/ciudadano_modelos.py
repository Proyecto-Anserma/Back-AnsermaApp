from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, field_serializer
from datetime import date
from typing import Any, Optional

from src.modulos.ubicacion.ubicacion_modelos import Ubicacion
from src.modulos.pertenencia_etnica.pertenencia_etnica_modelos import PertenenciaEtnica
from src.modulos.genero.genero_modelos import Genero



class CiudadanoBase(BaseModel):
    numero_identificacion_ciudadano: str
    nombre_ciudadano: str
    apellido_ciudadano: str
    fecha_nacimiento_ciudadano: date
    correo_electronico_ciudadano: str
    telefono_ciudadano: int
    id_ubicacion_ciudadano: int
    id_pertenencia_etnica_ciudadano: int
    id_genero_ciudadano: int

class CiudadanoCreate(CiudadanoBase):
    geolocalizacion: str

class Ciudadano(CiudadanoBase):
    geolocalizacion: Any
    numero_identificacion_ciudadano: str
    genero: Genero
    pertenencia_etnica: PertenenciaEtnica
    ubicacion: Ubicacion

    @field_serializer('geolocalizacion')
    def serialize_geometry(self, geom: Any) -> str:
        if isinstance(geom, WKBElement):
            return f"SRID=4326;{to_shape(geom).wkt}"
        return str(geom)

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
## ---------------------------------------------------------------

class CiudadanoResponse(CiudadanoBase):
    geolocalizacion: Any
    numero_identificacion_ciudadano: str
    genero:   Optional[Genero] = None
    pertenencia_etnica: Optional[PertenenciaEtnica] = None
    ubicacion: Optional[Ubicacion] = None

    @field_serializer('geolocalizacion')
    def serialize_geometry(self, geom: Any) -> str:
        if isinstance(geom, WKBElement):
            return f"SRID=4326;{to_shape(geom).wkt}"
        return str(geom)

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
## ---------------------------------------------------------------

class CiudadanosFiltrar(BaseModel):
    numero_identificacion_ciudadano: Optional[str] = None