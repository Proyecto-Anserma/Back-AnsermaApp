from pydantic import BaseModel

class TipoUbicacionBase(BaseModel):
    id_tipo_ubicacion: int
    descripcion_tipo_ubicacion: str

class TipoUbicacionCreate(TipoUbicacionBase):
    pass

class TipoUbicacion(TipoUbicacionBase):
    id_tipo_ubicacion: int

    class Config:
        orm_mode = True 
 