from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sql_update, delete as sql_delete
from .ubicacion_db_modelo import Ubicacion
from .ubicacion_modelos import UbicacionCreate, UbicacionUpdate

async def get_ubicaciones(db: AsyncSession):
    result = await db.execute(select(Ubicacion))
    return result.scalars().all()


async def create_ubicacion(db: AsyncSession, ubicacion_data: UbicacionCreate):
    nueva_ubicacion = Ubicacion(**ubicacion_data.model_dump())
    db.add(nueva_ubicacion)
    await db.commit()
    await db.refresh(nueva_ubicacion)
    return nueva_ubicacion

async def delete_ubicacion(db: AsyncSession, ubicacion_id: int):
    result = await db.execute(select(Ubicacion).where(Ubicacion.id_ubicacion == ubicacion_id))
    ubicacion = result.scalar_one_or_none()
    if ubicacion is None:
        return False
    await db.execute(sql_delete(Ubicacion).where(Ubicacion.id_ubicacion == ubicacion_id))
    await db.commit()
    return True

async def update_ubicacion(db: AsyncSession, ubicacion_id: int, ubicacion_data: UbicacionUpdate):
    result = await db.execute(select(Ubicacion).where(Ubicacion.id_ubicacion == ubicacion_id))
    ubicacion = result.scalar_one_or_none()
    if ubicacion is None:
        return None

    update_data = ubicacion_data.model_dump(exclude_unset=True)  # Solo actualizar campos enviados
    await db.execute(
        sql_update(Ubicacion)
        .where(Ubicacion.id_ubicacion == ubicacion_id)
        .values(**update_data)
    )
    await db.commit()
    await db.refresh(ubicacion)
    return ubicacion
