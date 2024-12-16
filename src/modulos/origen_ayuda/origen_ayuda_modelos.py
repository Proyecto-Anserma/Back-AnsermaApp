from pydantic import BaseModel
from typing import Optional

class OrigenAyudaBase(BaseModel):
    nombre_entidad_origen_ayuda: str
    nit: str
    telefono_origen_ayuda: float
    correo_electronico_origen_ayuda: str
    zona_territorial_origen_ayuda: str

    class Config:
        from_attributes = True

class OrigenAyudaCreate(OrigenAyudaBase):
    pass

class OrigenAyudaResponse(OrigenAyudaBase):
    id_origen_ayuda: int

    class Config:
        from_attributes = True

class OrigenAyudaFiltro(BaseModel):
    nit: Optional[str] = None
