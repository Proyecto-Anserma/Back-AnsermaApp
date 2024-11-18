from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, update as sql_update, delete as sql_delete
from .ayuda_db_modelo import Ayuda
from .ayuda_modelos import AyudaCreate

async def get_ayudas(db: AsyncSession):
    try:
        result = await db.execute(select(Ayuda))
        return result.scalars().all()
    except Exception as e:
        raise Exception(f"Error al obtener ayudas: {str(e)}")

async def create_ayuda(db: AsyncSession, ayuda_data: AyudaCreate):
    try:
        nueva_ayuda = Ayuda(**ayuda_data.dict())
        db.add(nueva_ayuda)
        await db.commit()
        await db.execute(
            text("SELECT setval('ayuda_id_ayuda_seq', (SELECT MAX(id_ayuda) FROM ayuda))")
        )
        await db.refresh(nueva_ayuda)
        return nueva_ayuda
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear ayuda: {str(e)}")

async def delete_ayuda(db: AsyncSession, ayuda_id: int):
    try:
        result = await db.execute(
            sql_delete(Ayuda)
            .where(Ayuda.id_ayuda == ayuda_id)
            .returning(Ayuda.id_ayuda)
        )
        deleted = result.scalar_one_or_none()
        await db.commit()
        return deleted is not None
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al eliminar ayuda: {str(e)}")
