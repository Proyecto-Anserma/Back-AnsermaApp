from pydantic import BaseModel
from datetime import date

class CiudadanoCreate(BaseModel):
    nombre_ciudadano: str
    apellido_ciudadano: str
    fecha_nacimiento_ciudadano: date
    correo_electronico_ciudadano: str
    telefono_ciudadano: str
    geolocalizacion: str
