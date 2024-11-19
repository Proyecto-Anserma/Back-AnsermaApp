from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, update as sql_update, delete as sql_delete
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
        nueva_solicitud_ayuda = SolicitudAyuda(**solicitud_ayuda_data.model_dump())
        db.add(nueva_solicitud_ayuda)
        await db.commit()
        await db.execute(
            text("SELECT setval('solicitud_ayuda_id_solicitud_ayuda_seq', (SELECT MAX(id_solicitud_ayuda) FROM solicitud_ayuda))")
        )
        await db.refresh(nueva_solicitud_ayuda)
        return nueva_solicitud_ayuda
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear solicitud de ayuda: {str(e)}")

    

async def update_solicitud_ayuda(
    db: AsyncSession, solicitud_ayuda_id: int, solicitud_ayuda_data: SolicitudAyudaCreate
):
    """
    Actualiza una solicitud de ayuda existente.

    :param db: Sesión de base de datos
    :param solicitud_ayuda_id: ID de la solicitud de ayuda a actualizar
    :param solicitud_ayuda_data: Datos nuevos para actualizar
    :return: La solicitud de ayuda actualizada o None si no se encuentra
    """
    try:
        result = await db.execute(
            sql_update(SolicitudAyuda)
            .where(SolicitudAyuda.id_solicitud_ayuda == solicitud_ayuda_id)
            .values(**solicitud_ayuda_data.dict())
            .returning(SolicitudAyuda)
        )
        updated_solicitud = result.scalar_one_or_none()
        if updated_solicitud:
            await db.commit()
            await db.refresh(updated_solicitud)
        return updated_solicitud
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al actualizar solicitud de ayuda: {str(e)}")


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
