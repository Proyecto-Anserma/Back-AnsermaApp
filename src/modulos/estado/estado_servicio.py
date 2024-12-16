from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .estado_db_modelo import Estado

async def get_estados(db: AsyncSession):
    result = await db.execute(select(Estado))
    return result.scalars().all()