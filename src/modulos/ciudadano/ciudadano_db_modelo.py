from geoalchemy2 import Geometry
from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.modulos import Base
from typing import Any, Optional
class Ciudadano(Base):
    __tablename__ = "ciudadano"
    numero_identificacion_ciudadano = Column(String, primary_key=True)
    nombre_ciudadano = Column(String, nullable=False)
    apellido_ciudadano = Column(String, nullable=False)
    fecha_nacimiento_ciudadano = Column(Date, nullable=False)
    correo_electronico_ciudadano = Column(String, unique=True, nullable=False)
    telefono_ciudadano = Column(Integer, nullable=True)
    geolocalizacion = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    id_ubicacion_ciudadano = Column(Integer, ForeignKey("ubicacion.id_ubicacion"), nullable=False)
    id_pertenencia_etnica_ciudadano = Column(Integer, ForeignKey("pertenencia_etnica.id_pertenencia_etnica"), nullable=False)
    id_genero_ciudadano = Column(Integer, ForeignKey("genero.id_genero"), nullable=False)

    # Relaciones para cargar automáticamente los valores de las tablas de referencia
    ubicacion = relationship("Ubicacion")
    pertenencia_etnica = relationship("PertenenciaEtnica")
    genero = relationship("Genero")


