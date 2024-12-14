from sqlalchemy import Column, Integer, String
from database.db_config import BaseAnserma

class Estado(BaseAnserma):
    __tablename__ = "estado"

    id_estado = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_estado = Column(String, nullable=False) 