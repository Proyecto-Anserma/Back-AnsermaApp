from pydantic import BaseModel

class EstadoBase(BaseModel):
    id_estado: int
    descripcion_estado: str

    class Config:
        from_attributes = True

class EstadoResponse(EstadoBase):
    pass
