from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database.db_config import BaseUsuarios

class Usuario(BaseUsuarios):
    __tablename__ = "usuario"

    numero_identificacion_usuario = Column(String, primary_key=True)
    nombre_usuario = Column(String, nullable=False)
    apellido_usuario = Column(String, nullable=False)
    fecha_nacimiento_usuario = Column(Date, nullable=False)
    correo_electronico_usuario = Column(String, nullable=True)
    telefono_usuario = Column(Integer, nullable=False)
    id_genero_usuario = Column(Integer, ForeignKey("genero.id_genero"), nullable=False)
    id_pertenencia_etnica_usuario = Column(Integer, ForeignKey("pertenencia_etnica.id_pertenencia_etnica"), nullable=False)
    id_ubicacion_usuario = Column(Integer, ForeignKey("ubicacion.id_ubicacion"), nullable=False)
    id_rol_usuario = Column(Integer, ForeignKey("rol.id_rol"), nullable=False)

