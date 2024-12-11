from pydantic import BaseModel, field_serializer
from datetime import date
from typing import Any, Optional
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape

from src.modulos.ubicacion.ubicacion_modelos import UbicacionBase
from src.modulos.pertenencia_etnica.pertenencia_etnica_modelos import PertenenciaEtnicaBase
from src.modulos.genero.genero_modelos import GeneroBase


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


class CiudadanoFiltrar(BaseModel):
    numero_identificacion_ciudadano: Optional[str] = None

class CiudadanoCreate(CiudadanoBase):
    geolocalizacion: Optional[str] = None

class CiudadanoResponse(CiudadanoBase):
    geolocalizacion: Optional[str]
    genero: GeneroBase
    pertenencia_etnica: PertenenciaEtnicaBase
    ubicacion: UbicacionBase

    @field_serializer('geolocalizacion')
    def serialize_geometry(self, geom: Any) -> Optional[str]:
        if isinstance(geom, WKBElement):
            return f"SRID=4326;{to_shape(geom).wkt}"
        return None if geom is None else str(geom)

    class Config:
        orm_mode = True
