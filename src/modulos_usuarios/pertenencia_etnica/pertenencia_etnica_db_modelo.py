from database.db_config import BaseAnserma 
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class PertenenciaEtnica(BaseAnserma):
    __tablename__ = "pertenencia_etnica"
    id_pertenencia_etnica = Column(Integer, primary_key=True, autoincrement=True)
    descripcion_pertenencia_etnica = Column(String, nullable=True)


    ciudadanos = relationship("Ciudadano", back_populates="pertenencia_etnica")