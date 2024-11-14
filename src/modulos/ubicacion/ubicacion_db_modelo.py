from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ubicacion(Base):
    __tablename__ = "ubicacion"
    
    id_ubicacion = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_ubicacion = Column(String, nullable=False)
    id_tipo_ubicacion = Column(Integer, ForeignKey("tipo_ubicacion.id_tipo_ubicacion"), nullable=False)