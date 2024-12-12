
from .pertenencia_etnica_db_modelo import *
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_pertenencia_etnica(db: AsyncSession):
    result = await db.execute(select(PertenenciaEtnica))
    return result.scalars().all()