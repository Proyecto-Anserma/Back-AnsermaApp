from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db_config import BaseAnserma 

class TipoUbicacion(BaseAnserma):
    __tablename__ = "tipo_ubicacion"
    id_tipo_ubicacion = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_tipo_ubicacion = Column(String, nullable=True)

    ubicaciones = relationship("Ubicacion", back_populates="tipo_ubicacion")

    