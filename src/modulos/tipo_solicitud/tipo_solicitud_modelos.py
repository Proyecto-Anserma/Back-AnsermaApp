from pydantic import BaseModel


class TipoSolicitudBase(BaseModel):
    id_tipo_solicitud: int
    descripcion_tipo_solicitud: str

class TipoSolicitudCreate(TipoSolicitudBase):
    pass

class TipoSolicitudResponse(TipoSolicitudBase):
    id_tipo_solicitud: int

    class Config:
        orm_mode = True 
 