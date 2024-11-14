from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .ubicacion_db_modelo import Ubicacion

async def get_ubicaciones(db: AsyncSession):
    result = await db.execute(select(Ubicacion))
    return result.scalars().all()