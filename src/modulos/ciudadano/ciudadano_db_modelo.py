from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship

Base = declarative_base()

class Ciudadano(Base):
    __tablename__ = "ciudadano"
    
    numero_identificacion_ciudadano = Column(String, primary_key=True)
    nombre_ciudadano = Column(String, nullable=False)
    apellido_ciudadano = Column(String, nullable=False)
    fecha_nacimiento_ciudadano = Column(Date, nullable=False)
    correo_electronico_ciudadano = Column(String, unique=True, nullable=False)
    telefono_ciudadano = Column(String, nullable=True)
    geolocalizacion = Column(Geometry("POINT"), nullable=True)
    id_ubicacion_ciudadano = Column(Integer, ForeignKey("ubicacion.id_ubicacion"), nullable=False)
    id_pertenencia_etnica_ciudadano = Column(Integer, ForeignKey("pertenencia_etnica.id_pertenencia_etnica"), nullable=False)
    id_genero_ciudadano = Column(Integer, ForeignKey("genero.id_genero"), nullable=False)

    # Relaciones para cargar automáticamente los valores de las tablas de referencia
    ubicacion = relationship("Ubicacion")
    pertenencia_etnica = relationship("PertenenciaEtnica")
    genero = relationship("Genero")