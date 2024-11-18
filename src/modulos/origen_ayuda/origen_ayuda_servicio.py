from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sql_update, delete as sql_delete
from .origen_ayuda_db_modelo import OrigenAyuda
from .origen_ayuda_modelos import OrigenAyudaCreate

async def get_origenes_ayuda(db: AsyncSession):
    try:
        result = await db.execute(select(OrigenAyuda))
        return result.scalars().all()
    except Exception as e:
        raise Exception(f"Error al obtener orígenes de ayuda: {str(e)}")

async def create_origen_ayuda(db: AsyncSession, origen_ayuda_data: OrigenAyudaCreate):
    try:
        nuevo_origen_ayuda = OrigenAyuda(**origen_ayuda_data.dict())
        db.add(nuevo_origen_ayuda)
        await db.commit()
        await db.refresh(nuevo_origen_ayuda)
        return nuevo_origen_ayuda
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear origen de ayuda: {str(e)}")

async def delete_origen_ayuda(db: AsyncSession, origen_ayuda_id: int):
    try:
        result = await db.execute(
            sql_delete(OrigenAyuda)
            .where(OrigenAyuda.id_origen_ayuda == origen_ayuda_id)
            .returning(OrigenAyuda.id_origen_ayuda)
        )
        deleted = result.scalar_one_or_none()
        await db.commit()
        return deleted is not None
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al eliminar origen de ayuda: {str(e)}")
