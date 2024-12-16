from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database.db_config import BaseAnserma

class Ayuda(BaseAnserma):
    __tablename__ = "ayuda"

    id_ayuda = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_solicitud = Column(String(250), nullable=False)
    fecha_creacion_ayuda = Column(Date, nullable=False)
    observacion_ayuda = Column(String(500), nullable=False)
    foto_solicitud = Column(String, nullable=False)

    # Relaciones
    solicitudes_ayuda = relationship("SolicitudAyuda", back_populates="ayuda")
    cantidades_origen_ayuda = relationship("CantidadOrigenAyuda", back_populates="ayuda")
