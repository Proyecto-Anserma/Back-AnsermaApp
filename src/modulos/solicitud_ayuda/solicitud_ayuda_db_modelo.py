from sqlalchemy import Column, Integer, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from database.db_config import BaseAnserma 


class SolicitudAyuda(BaseAnserma):
    __tablename__ = "solicitud_ayuda"

    id_solicitud_ayuda = Column(Integer, primary_key=True, index=True)
    cantidad_solicitud_ayuda = Column(Integer, nullable=False)
    fecha_entrega_solicitud_ayuda = Column(Date, nullable=False)
    foto_entrega_solicitud_ayuda = Column(Text, nullable=False)
    id_solicitud = Column(Integer, ForeignKey("solicitud.id_solicitud", ondelete="CASCADE"), nullable=False)
    id_ayuda = Column(Integer, ForeignKey("ayuda.id_ayuda", ondelete="CASCADE"), nullable=False)

    # Definir las relaciones
    solicitud = relationship("Solicitud", back_populates="solicitudes_ayuda")
    ayuda = relationship("Ayuda", back_populates="solicitudes_ayuda")

   