from pydantic import BaseModel
from datetime import date
from typing import Optional

class CantidadOrigenAyudaBase(BaseModel):
    cantidad_origen_ayuda: int

class CantidadOrigenAyudaCreate(CantidadOrigenAyudaBase):
    id_origen_ayuda: int
    id_ayuda: int
    fecha_entrega_cantidad_origen_ayuda: Optional[date] = None

class CantidadOrigenAyudaResponse(CantidadOrigenAyudaBase):
    id_cantidad_origen_ayuda: int
    id_origen_ayuda: int
    id_ayuda: int
    fecha_entrega_cantidad_origen_ayuda: date

    class Config:
        from_attributes = True
