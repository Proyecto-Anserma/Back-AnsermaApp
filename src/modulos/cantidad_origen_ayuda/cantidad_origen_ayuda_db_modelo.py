from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.modulos import Base

class CantidadOrigenAyuda(Base):
    __tablename__ = "cantidad_origen_ayuda"

    id_cantidad_origen_ayuda = Column(Integer, primary_key=True, index=True)
    cantidad_origen_ayuda = Column(Integer, nullable=False)
    fecha_entrega_cantidad_origen_ayuda = Column(Date, nullable=False)
    id_origen_ayuda = Column(Integer, ForeignKey("origen_ayuda.id_origen_ayuda", ondelete="CASCADE"), nullable=False)
    id_ayuda = Column(Integer, ForeignKey("ayuda.id_ayuda", ondelete="CASCADE"), nullable=False)

    origen_ayuda = relationship("OrigenAyuda")
    ayuda = relationship("Ayuda")
