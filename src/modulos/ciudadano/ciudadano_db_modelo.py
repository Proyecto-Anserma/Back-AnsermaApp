from geoalchemy2 import Geometry
from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.db_config import BaseAnserma


class Ciudadano(BaseAnserma):
    __tablename__ = "ciudadano"

    numero_identificacion_ciudadano = Column(String, primary_key=True, index=True)
    nombre_ciudadano = Column(String, nullable=False)
    apellido_ciudadano = Column(String, nullable=False)
    fecha_nacimiento_ciudadano = Column(Date, nullable=False)
    correo_electronico_ciudadano = Column(String, unique=True, nullable=False)
    telefono_ciudadano = Column(Integer, nullable=True)
    id_ubicacion_ciudadano = Column(Integer, ForeignKey("ubicacion.id_ubicacion"), nullable=False)
    id_pertenencia_etnica_ciudadano = Column(Integer, ForeignKey("pertenencia_etnica.id_pertenencia_etnica"), nullable=False)
    id_genero_ciudadano = Column(Integer, ForeignKey("genero.id_genero"), nullable=False)
    geolocalizacion = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)

    # Relaciones para cargar automáticamente los valores de las tablas de referencia
    genero = relationship("Genero", back_populates="ciudadanos")
    pertenencia_etnica = relationship("PertenenciaEtnica", back_populates="ciudadanos")
    ubicacion = relationship("Ubicacion", back_populates="ciudadanos")
