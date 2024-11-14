from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship

Base = declarative_base()

class Solicitud(Base):
    __tablename__ = "solicitud"
    
    id_solicitud = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_solicitud = Column(String, nullable=False)
    fecha_creacion_solicitud = Column(Date, nullable=False)
    foto_solicitud = Column(String, nullable=True)
    geolocalizacion = Column(Geometry("POINT"), nullable=True)
    id_tipo_solicitud = Column(Integer, ForeignKey("tipo_solicitud.id_tipo_solicitud"), nullable=False)
    id_ubicacion_solicitud = Column(Integer, ForeignKey("ubicacion.id_ubicacion"), nullable=False)
    id_ciudadano_solicitud = Column(Integer, ForeignKey("ciudadano.id_ciudadano"), nullable=False)

    # Relaciones para cargar automáticamente los valores de las tablas de referencia
    tipo_solicitud = relationship("TipoSolicitud")
    ubicacion = relationship("Ubicacion")
    ciudadano = relationship("Ciudadano")