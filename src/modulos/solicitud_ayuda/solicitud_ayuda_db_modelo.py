from sqlalchemy import Column, Integer, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from src.modulos import Base

class SolicitudAyuda(Base):
    __tablename__ = "solicitud_ayuda"

    id_solicitud_ayuda = Column(Integer, primary_key=True, index=True)
    cantidad_solicitud_ayuda = Column(Integer, nullable=False)
    fecha_entrega_solicitud_ayuda = Column(Date, nullable=False)
    foto_entrega_solicitud_ayuda = Column(Text, nullable=False)
    id_solicitud = Column(Integer, ForeignKey("solicitud.id_solicitud", ondelete="CASCADE"), nullable=False)
    id_ayuda = Column(Integer, ForeignKey("ayuda.id_ayuda", ondelete="CASCADE"), nullable=False)

    solicitud = relationship("Solicitud")
    ayuda = relationship("Ayuda")
