from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .solicitud_db_modelo import Solicitud

async def get_solicitudes(db: AsyncSession):
    result = await db.execute(select(Solicitud))
    return result.scalars().all()
