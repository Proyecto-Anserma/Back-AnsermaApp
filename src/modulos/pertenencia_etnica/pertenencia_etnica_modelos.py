from pydantic import BaseModel


class PertenenciaEtnicaBase(BaseModel):
    id_pertenencia_etnica: int
    descripcion_pertenencia_etnica: str

class PertenenciaEtnicaCreate(PertenenciaEtnicaBase):
    pass

class PertenenciaEtnicaResponse(PertenenciaEtnicaBase):
    id_pertenencia_etnica: int

    class Config:
        orm_mode = True 
 