from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sql_update, delete as sql_delete
from .solicitud_ayuda_db_modelo import SolicitudAyuda
from .solicitud_ayuda_modelos import SolicitudAyudaCreate

async def get_solicitudes_ayuda(db: AsyncSession):
    try:
        result = await db.execute(select(SolicitudAyuda))
        return result.scalars().all()
    except Exception as e:
        raise Exception(f"Error al obtener solicitudes de ayuda: {str(e)}")

async def create_solicitud_ayuda(db: AsyncSession, solicitud_ayuda_data: SolicitudAyudaCreate):
    try:
        nueva_solicitud_ayuda = SolicitudAyuda(**solicitud_ayuda_data.dict())
        db.add(nueva_solicitud_ayuda)
        await db.commit()
        await db.refresh(nueva_solicitud_ayuda)
        return nueva_solicitud_ayuda
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear solicitud de ayuda: {str(e)}")

async def delete_solicitud_ayuda(db: AsyncSession, solicitud_ayuda_id: int):
    try:
        result = await db.execute(
            sql_delete(SolicitudAyuda)
            .where(SolicitudAyuda.id_solicitud_ayuda == solicitud_ayuda_id)
            .returning(SolicitudAyuda.id_solicitud_ayuda)
        )
        deleted = result.scalar_one_or_none()
        await db.commit()
        return deleted is not None
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al eliminar solicitud de ayuda: {str(e)}")
