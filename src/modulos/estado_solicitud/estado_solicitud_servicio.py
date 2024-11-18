from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, update as sql_update, delete as sql_delete
from .estado_solicitud_db_modelo import EstadoSolicitud
from .estado_solicitud_modelos import EstadoSolicitudUpdate

async def get_estado_solicitudes(db: AsyncSession):
    try:
        result = await db.execute(select(EstadoSolicitud))
        return result.scalars().all()
    except Exception as e:
        raise Exception(f"Error al obtener estados de solicitud: {str(e)}")

async def create_estado_solicitud(db: AsyncSession, estado_solicitud_data: dict):
    try:
        nuevo_estado_solicitud = EstadoSolicitud(**estado_solicitud_data)
        db.add(nuevo_estado_solicitud)
        await db.commit()
        await db.execute(
            text("SELECT setval('estado_solicitud_id_estado_solicitud_seq', (SELECT MAX(id_estado_solicitud) FROM estado_solicitud))")
        )
        
        await db.refresh(nuevo_estado_solicitud)
        return nuevo_estado_solicitud
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear estado de solicitud: {str(e)}")

async def update_estado_solicitud(db: AsyncSession, estado_solicitud_id: int, estado_solicitud_data: EstadoSolicitudUpdate):
    try:
        result = await db.execute(select(EstadoSolicitud).where(EstadoSolicitud.id_estado_solicitud == estado_solicitud_id))
        estado_solicitud = result.scalar_one_or_none()
        if estado_solicitud is None:
            return None

        update_data = estado_solicitud_data.model_dump(exclude_unset=True)
        await db.execute(
            sql_update(EstadoSolicitud)
            .where(EstadoSolicitud.id_estado_solicitud == estado_solicitud_id)
            .values(**update_data)
        )
        await db.commit()
        await db.refresh(estado_solicitud)
        return estado_solicitud
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al actualizar estado de solicitud: {str(e)}")

async def delete_estado_solicitud(db: AsyncSession, estado_solicitud_id: int):
    try:
        result = await db.execute(
            sql_delete(EstadoSolicitud)
            .where(EstadoSolicitud.id_estado_solicitud == estado_solicitud_id)
            .returning(EstadoSolicitud.id_estado_solicitud)
        )
        deleted = result.scalar_one_or_none()
        await db.commit()
        return deleted is not None
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al eliminar estado de solicitud: {str(e)}")
