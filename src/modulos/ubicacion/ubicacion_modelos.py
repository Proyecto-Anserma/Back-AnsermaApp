from pydantic import BaseModel
from datetime import date
from typing import Optional

class UbicacionBase(BaseModel):
    descripcion_ubicacion: str
    id_tipo_ubicacion: int

class UbicacionCreate(UbicacionBase):
    pass

class UbicacionUpdate(UbicacionBase):
    pass