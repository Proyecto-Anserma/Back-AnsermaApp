from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db_config import BaseAnserma 

class Ubicacion(BaseAnserma):
    __tablename__ = "ubicacion"
    
    id_ubicacion = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_ubicacion = Column(String, nullable=False)
    id_tipo_ubicacion = Column(Integer, ForeignKey("tipo_ubicacion.id_tipo_ubicacion"), nullable=False)


    ciudadanos = relationship("Ciudadano", back_populates="ubicacion")
    solicitudes = relationship("Solicitud", back_populates="ubicacion")

    
    tipo_ubicacion = relationship("TipoUbicacion", back_populates="ubicaciones")