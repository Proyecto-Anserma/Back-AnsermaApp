from pydantic import BaseModel
from datetime import date
from typing import Optional

class UbicacionBase(BaseModel):
    id_ubicacion: int
    descripcion_ubicacion: str
    id_tipo_ubicacion: int

class UbicacionCreate(UbicacionBase):
    pass

class Ubicacion(UbicacionBase):
    id_ubicacion: int

    class Config:
        orm_mode = True 

#------------------------------------

class UbicacionUpdate(UbicacionBase):
    pass