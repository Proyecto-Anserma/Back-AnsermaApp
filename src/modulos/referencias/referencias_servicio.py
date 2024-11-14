from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .referencias_db_modelo import TipoSolicitud, Genero, TipoUbicacion, PertenenciaEtnica

async def get_tipo_solicitudes(db: AsyncSession):
    result = await db.execute(select(TipoSolicitud))
    return result.scalars().all()

async def get_tipo_ubicaciones(db: AsyncSession):
    result = await db.execute(select(TipoUbicacion))
    return result.scalars().all()

async def get_generos(db: AsyncSession):
    result = await db.execute(select(Genero))
    return result.scalars().all()

async def get_pertenencia_etnica(db: AsyncSession):
    result = await db.execute(select(PertenenciaEtnica))
    return result.scalars().all()

