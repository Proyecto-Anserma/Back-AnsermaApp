from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, update as sql_update, delete as sql_delete
from .ubicacion_db_modelo import Ubicacion
from .ubicacion_modelos import UbicacionCreate, UbicacionUpdate, UbicacionResponse

async def get_ubicaciones(db: AsyncSession):
    """
    Obtiene todas las ubicaciones de la base de datos.
    """
    try:
        result = await db.execute(select(UbicacionResponse))
        return result.scalars().all()
    except Exception as e:
        raise Exception(f"Error al obtener ubicaciones: {str(e)}")
    

async def create_ubicacion(db: AsyncSession, ubicacion_data: UbicacionCreate):
    """
    Crea una nueva ubicación.
    """
    try:
        nueva_ubicacion = Ubicacion(**ubicacion_data.model_dump())
        db.add(nueva_ubicacion)
        await db.commit()
        await db.execute(
            text("SELECT setval('ubicacion_id_ubicacion_seq', (SELECT MAX(id_ubicacion) FROM ubicacion))")
        )
        
        await db.refresh(nueva_ubicacion)
        return nueva_ubicacion
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear ubicación: {str(e)}")
    

async def update_ubicacion(db: AsyncSession, ubicacion_id: int, ubicacion_data: UbicacionUpdate):
    """
    Actualiza una ubicación existente.
    """
    try:
        result = await db.execute(select(Ubicacion).where(Ubicacion.id_ubicacion == ubicacion_id))
        ubicacion = result.scalar_one_or_none()
        if not ubicacion:
            return None

        update_data = ubicacion_data.model_dump(exclude_unset=True)
        await db.execute(
            sql_update(Ubicacion)
            .where(Ubicacion.id_ubicacion == ubicacion_id)
            .values(**update_data)
        )
        await db.commit()
        await db.refresh(ubicacion)
        return ubicacion
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al actualizar ubicación: {str(e)}")

async def delete_ubicacion(db: AsyncSession, ubicacion_id: int):
    """
    Elimina una ubicación por su ID.
    """
    try:
        result = await db.execute(select(Ubicacion).where(Ubicacion.id_ubicacion == ubicacion_id))
        ubicacion = result.scalar_one_or_none()
        if not ubicacion:
            return False

        await db.execute(sql_delete(Ubicacion).where(Ubicacion.id_ubicacion == ubicacion_id))
        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al eliminar ubicación: {str(e)}")
