from pydantic import BaseModel


class GeneroBase(BaseModel):
    id_genero: int
    descripcion_genero: str

class GeneroCreate(GeneroBase):
    pass

class GeneroResponse(GeneroBase):
    id_genero: int

    class Config:
        orm_mode = True 
 