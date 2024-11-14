from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database
from contextlib import asynccontextmanager

# URL de conexión a la base de datos
DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/AnsermaApp"

# Crea el motor asíncrono de SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Configura la sesión de SQLAlchemy
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Usa 'Database' para la conexión asíncrona con databases
database = Database(DATABASE_URL)

# Base de SQLAlchemy para los modelos
Base = declarative_base()

# Define la dependencia get_db para usar en los endpoints de FastAPI
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

