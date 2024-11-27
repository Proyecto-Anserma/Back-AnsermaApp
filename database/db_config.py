
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database

# Configuración de la base de datos Anserma
DATABASE_URL_ANSERMA = "postgresql+asyncpg://postgres:admin@localhost:5432/AnsermaApp"
engine_anserma = create_async_engine(DATABASE_URL_ANSERMA, echo=True)
async_session_anserma = sessionmaker(bind=engine_anserma, class_=AsyncSession, expire_on_commit=False)
database_anserma = Database(DATABASE_URL_ANSERMA)
BaseAnserma = declarative_base()

# Configuración de la base de datos Usuarios
DATABASE_URL_USUARIOS = "postgresql+asyncpg://postgres:admin@localhost:5432/AnsermaApp_Registro_Usuario"
engine_usuarios = create_async_engine(DATABASE_URL_USUARIOS, echo=True)
async_session_usuarios = sessionmaker(bind=engine_usuarios, class_=AsyncSession, expire_on_commit=False)
database_usuarios = Database(DATABASE_URL_USUARIOS)
BaseUsuarios = declarative_base()

from src.modulos.ciudadano.ciudadano_db_modelo import Ciudadano
from src.modulos.genero.genero_db_modelo import Genero

# Funciones para obtener sesiones de las bases de datos
async def get_db_anserma():
    async with async_session_anserma() as session:
        yield session

async def get_db_usuarios():
    async with async_session_usuarios() as session:
        yield session
