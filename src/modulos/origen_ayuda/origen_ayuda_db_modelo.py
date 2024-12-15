from sqlalchemy import Column, Integer, String, Numeric
from database.db_config import BaseAnserma

class OrigenAyuda(BaseAnserma):
    __tablename__ = "origen_ayuda"

    id_origen_ayuda = Column(Integer, primary_key=True, autoincrement=True)
    nombre_entidad_origen_ayuda = Column(String(100))
    nit = Column(String(50))
    telefono_origen_ayuda = Column(Numeric(50))
    correo_electronico_origen_ayuda = Column(String(100))
    zona_territorial_origen_ayuda = Column(String(100))
