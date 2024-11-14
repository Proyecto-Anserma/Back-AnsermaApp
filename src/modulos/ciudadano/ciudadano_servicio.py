from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .ciudadano_db_modelo import Ciudadano

async def get_ciudadanos(db: AsyncSession):
    result = await db.execute(select(Ciudadano))
    return result.scalars().all()
