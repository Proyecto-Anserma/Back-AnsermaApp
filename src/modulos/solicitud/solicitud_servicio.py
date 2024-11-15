from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sql_update, delete as sql_delete
from .solicitud_db_modelo import Solicitud
from .solicitud_modelos import SolicitudCreate, SolicitudUpdate

async def get_solicitudes(db: AsyncSession):
    result = await db.execute(select(Solicitud))
    return result.scalars().all()

async def create_solicitud(db: AsyncSession, solicitud_data: SolicitudCreate):
    nueva_solicitud = Solicitud(**solicitud_data.model_dump())
    db.add(nueva_solicitud)
    await db.commit()
    await db.refresh(nueva_solicitud)
    return nueva_solicitud

async def delete_solicitud(db: AsyncSession, solicitud_id: int):
    result = await db.execute(select(Solicitud).where(Solicitud.id_solicitud == solicitud_id))
    solicitud = result.scalar_one_or_none()
    if solicitud is None:
        return False
    await db.execute(sql_delete(Solicitud).where(Solicitud.id_solicitud == solicitud_id))
    await db.commit()
    return True

async def update_solicitud(db: AsyncSession, solicitud_id: int, solicitud_data: SolicitudUpdate):
    result = await db.execute(select(Solicitud).where(Solicitud.id_solicitud == solicitud_id))
    solicitud = result.scalar_one_or_none()
    if solicitud is None:
        return None

    update_data = solicitud_data.model_dump(exclude_unset=True)  # Solo actualizar campos enviados
    await db.execute(
        sql_update(Solicitud)
        .where(Solicitud.id_solicitud == solicitud_id)
        .values(**update_data)
    )
    await db.commit()
    await db.refresh(solicitud)
    return solicitud
