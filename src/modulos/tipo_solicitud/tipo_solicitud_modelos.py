from pydantic import BaseModel


class TipoSolicitudBase(BaseModel):
    id_tipo_solicitud: int
    descripcion_tipo_solicitud: str

class PertenenciaEtnicaCreate(TipoSolicitudBase):
    pass

class PertenenciaEtnica(TipoSolicitudBase):
    id_tipo_solicitud: int

    class Config:
        orm_mode = True 
 