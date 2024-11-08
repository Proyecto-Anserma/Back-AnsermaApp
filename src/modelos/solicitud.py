from pydantic import BaseModel
from datetime import date

class Solicitud(BaseModel):
    descripcion_solicitud: str
    fecha_creacion_solicitud: date
    foto_solicitud: str
    geolocalizacion: str
    tipo_solicitud: int
    ubicacion_solicitud: int
    ciudadano_solicitud: int