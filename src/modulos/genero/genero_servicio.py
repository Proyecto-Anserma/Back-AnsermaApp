
from .genero_db_modelo import *
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_genero(db: AsyncSession):
    result = await db.execute(select(Genero))
    return result.scalars().all()