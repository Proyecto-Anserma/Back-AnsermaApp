from database.db_config import BaseAnserma 
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Genero(BaseAnserma):
    __tablename__ = "genero"
    id_genero = Column(Integer, primary_key=True, autoincrement=True, index=True)
    descripcion_genero = Column(String, nullable=True)

    ciudadanos = relationship("Ciudadano", back_populates="genero")