from sqlalchemy import Column, Integer, String, Date, Text
from database.db_config import BaseAnserma 

class Ayuda(BaseAnserma):
    __tablename__ = "ayuda"

    id_ayuda = Column(Integer, primary_key=True, index=True)
    descripcion_solicitud = Column(String(250), nullable=False)
    fecha_creacion_ayuda = Column(Date, nullable=False)
    observacion_ayuda = Column(String(500), nullable=False)
    foto_solicitud = Column(Text, nullable=False)
