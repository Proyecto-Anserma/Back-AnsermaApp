from sqlalchemy import Column, Integer, String, Date
from src.modulos import Base

class TipoUbicacion(Base):
    __tablename__ = "tipo_ubicacion"
    id_tipo_ubicacion = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_tipo_ubicacion = Column(String, nullable=True)

class TipoSolicitud(Base):
    __tablename__ = "tipo_solicitud"
    id_tipo_solicitud = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_tipo_solicitud = Column(String, nullable=True)

class Genero(Base):
    __tablename__ = "genero"
    id_genero = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_genero = Column(String, nullable=True)

class PertenenciaEtnica(Base):
    __tablename__ = "pertenencia_etnica"
    id_pertenencia_etnica = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_pertenencia_etnica = Column(String, nullable=True)

class Rol(Base):
    __tablename__ = "rol"
    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_rol = Column(String, nullable=True)
    fecha_creacion_rol = Column(Date, nullable=True)

class Estado(Base):
    __tablename__ = "estado"
    id_estado = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_estado = Column(String, nullable=True)