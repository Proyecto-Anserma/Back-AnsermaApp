from sqlalchemy import Column, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.db_config import BaseAnserma 

class EstadoSolicitud(BaseAnserma):
    __tablename__ = "estado_solicitud"
    
    id_estado_solicitud = Column(Integer, primary_key=True, autoincrement=True)
    fecha_cambio_estado_solicitud = Column(Date, nullable=False)
    id_solicitud = Column(Integer, ForeignKey("solicitud.id_solicitud", ondelete="CASCADE"), nullable=False)
    id_estado = Column(Integer, ForeignKey("estado.id_estado", ondelete="CASCADE"), nullable=False)

