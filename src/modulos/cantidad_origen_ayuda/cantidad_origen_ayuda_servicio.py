from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sql_update, delete as sql_delete
from .cantidad_origen_ayuda_db_modelo import CantidadOrigenAyuda
from .cantidad_origen_ayuda_modelos import CantidadOrigenAyudaCreate

async def get_cantidades_origen_ayuda(db: AsyncSession):
    try:
        result = await db.execute(select(CantidadOrigenAyuda))
        return result.scalars().all()
    except Exception as e:
        raise Exception(f"Error al obtener cantidades de origen de ayuda: {str(e)}")

async def create_cantidad_origen_ayuda(db: AsyncSession, cantidad_origen_ayuda_data: CantidadOrigenAyudaCreate):
    try:
        nueva_cantidad_origen_ayuda = CantidadOrigenAyuda(**cantidad_origen_ayuda_data.dict())
        db.add(nueva_cantidad_origen_ayuda)
        await db.commit()
        await db.refresh(nueva_cantidad_origen_ayuda)
        return nueva_cantidad_origen_ayuda
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear cantidad de origen de ayuda: {str(e)}")

async def delete_cantidad_origen_ayuda(db: AsyncSession, cantidad_origen_ayuda_id: int):
    try:
        result = await db.execute(
            sql_delete(CantidadOrigenAyuda)
            .where(CantidadOrigenAyuda.id_cantidad_origen_ayuda == cantidad_origen_ayuda_id)
            .returning(CantidadOrigenAyuda.id_cantidad_origen_ayuda)
        )
        deleted = result.scalar_one_or_none()
        await db.commit()
        return deleted is not None
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al eliminar cantidad de origen de ayuda: {str(e)}")
