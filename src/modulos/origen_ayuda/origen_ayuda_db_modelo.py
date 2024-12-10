from sqlalchemy import Column, Integer, String, Numeric
from src.modulos import Base

class OrigenAyuda(Base):
    __tablename__ = "origen_ayuda"

    id_origen_ayuda = Column(Integer, primary_key=True, index=True)
    nombre_entidad_origen_ayuda = Column(String(100), nullable=False)
    nit = Column(String(50), nullable=False)
    telefono_origen_ayuda = Column(Numeric(50), nullable=False)
    correo_electronico_origen_ayuda = Column(String(100), nullable=False)
    zona_territorial_origen_ayuda = Column(String(100), nullable=False)
