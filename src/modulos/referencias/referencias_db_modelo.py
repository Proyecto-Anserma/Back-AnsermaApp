from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TipoUbicacion(Base):
    __tablename__ = "tipo_ubicacion"
    
    id_tipo_ubicacion = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_tipo_ubicacion = Column(String, nullable=False)
    

class TipoSolicitud(Base):
    __tablename__ = "tipo_solicitud"
    
    id_tipo_solicitud = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_tipo_solicitud = Column(String, nullable=False)
    

class Genero(Base):
    __tablename__ = "genero"
    
    id_genero = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_genero = Column(String, nullable=False)
    
    
class PertenenciaEtnica(Base):
    __tablename__ = "pertenencia_etnica"
    
    id_pertenencia_etnica = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_pertenencia_etnica = Column(String, nullable=False)