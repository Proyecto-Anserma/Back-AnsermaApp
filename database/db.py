from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from databases import Database

# URL de conexión a la base de datos
DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/AnsermaApp"

# Crea el motor asíncrono de SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Crea la sesión asíncrona de SQLAlchemy
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Usar 'Database' de databases para la conexión asíncrona
database = Database(DATABASE_URL)
