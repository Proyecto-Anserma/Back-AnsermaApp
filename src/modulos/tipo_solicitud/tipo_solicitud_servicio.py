
from .tipo_solicitud_db_modelo import *
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_tipo_solicitud(db: AsyncSession):
    result = await db.execute(select(TipoSolicitud))
    return result.scalars().all()