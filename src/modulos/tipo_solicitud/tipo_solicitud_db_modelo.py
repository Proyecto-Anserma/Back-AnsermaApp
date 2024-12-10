from sqlalchemy import Column, Integer, String, Date
from database.db_config import BaseAnserma 
from sqlalchemy.orm import relationship


class TipoSolicitud(BaseAnserma):
    __tablename__ = "tipo_solicitud"
    id_tipo_solicitud = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_tipo_solicitud = Column(String, nullable=True)

    solicitudes = relationship("Solicitud", back_populates="tipo_solicitud")