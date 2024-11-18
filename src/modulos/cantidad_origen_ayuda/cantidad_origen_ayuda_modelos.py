from pydantic import BaseModel
from datetime import date

class CantidadOrigenAyudaBase(BaseModel):
    cantidad_origen_ayuda: int
    fecha_entrega_cantidad_origen_ayuda: date

class CantidadOrigenAyudaCreate(CantidadOrigenAyudaBase):
    id_origen_ayuda: int
    id_ayuda: int

class CantidadOrigenAyudaResponse(CantidadOrigenAyudaBase):
    id_cantidad_origen_ayuda: int
    id_origen_ayuda: int
    id_ayuda: int

    class Config:
        orm_mode = True
