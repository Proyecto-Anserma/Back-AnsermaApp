from sqlalchemy import Column, Integer, String, Date, ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship
from src.modulos import Base

class Solicitud(Base):
    __tablename__ = "solicitud"
    
    id_solicitud = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_solicitud = Column(String, nullable=False)
    fecha_creacion_solicitud = Column(Date, nullable=False)
    foto_solicitud = Column(String, nullable=True)
    geolocalizacion = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    id_tipo_solicitud = Column(Integer, ForeignKey("tipo_solicitud.id_tipo_solicitud"), nullable=False)
    id_ubicacion_solicitud = Column(Integer, ForeignKey("ubicacion.id_ubicacion"), nullable=False)
    id_ciudadano_solicitud = Column(String, ForeignKey("ciudadano.numero_identificacion_ciudadano"), nullable=False)

    # Relaciones para cargar automáticamente los valores de las tablas de referencia
    tipo_solicitud = relationship("TipoSolicitud")
    ubicacion = relationship("Ubicacion")
    ciudadano = relationship("Ciudadano")