from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, update as sql_update, delete as sql_delete
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
        nuevo_origen_ayuda = OrigenAyuda(**origen_ayuda_data.model_dump())
        db.add(nuevo_origen_ayuda)
        await db.commit()
        await db.execute(
            text("SELECT setval('origen_ayuda_id_origen_ayuda_seq', (SELECT MAX(id_origen_ayuda) FROM origen_ayuda))")
        )
        await db.refresh(nuevo_origen_ayuda)
        return nuevo_origen_ayuda
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear origen de ayuda: {str(e)}")

    
async def update_origen_ayuda(
    db: AsyncSession, origen_ayuda_id: int, origen_ayuda_data: OrigenAyudaCreate
):
    """
    Actualiza un origen de ayuda existente.

    :param db: Sesión de base de datos
    :param origen_ayuda_id: ID del origen de ayuda a actualizar
    :param origen_ayuda_data: Datos nuevos para actualizar
    :return: El origen de ayuda actualizado o None si no se encuentra
    """
    try:
        result = await db.execute(
            sql_update(OrigenAyuda)
            .where(OrigenAyuda.id_origen_ayuda == origen_ayuda_id)
            .values(**origen_ayuda_data.dict())
            .returning(OrigenAyuda)
        )
        updated_origen = result.scalar_one_or_none()
        if updated_origen:
            await db.commit()
            await db.refresh(updated_origen)
        return updated_origen
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al actualizar origen de ayuda: {str(e)}")


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

async def filtrar_origen_ayuda_por_nit(db: AsyncSession, nit: str):
    try:
        query = select(OrigenAyuda)
        
        if nit:
            query = query.where(OrigenAyuda.nit == nit)
            
        result = await db.execute(query)
        return result.scalars().all()
        
    except Exception as e:
        raise Exception(f"Error al filtrar origen ayuda: {str(e)}")
