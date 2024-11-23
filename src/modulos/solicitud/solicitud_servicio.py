from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, select, update as sql_update, delete as sql_delete
from .solicitud_db_modelo import Solicitud
from .solicitud_modelos import SolicitudUpdate, SolicitudFiltrar

async def get_solicitudes(db: AsyncSession):
    try:
        result = await db.execute(select(Solicitud))
        return result.scalars().all()
    except Exception as e:
        raise Exception(f"Error al obtener solicitudes: {str(e)}")
    

async def filtrar_solicitudes(
    db: AsyncSession, 
    filtros: SolicitudFiltrar
):
    """
    Filtra solicitudes por descripción y/o id_ciudadano_solicitud.
    Si no se proporcionan filtros, devuelve todas las solicitudes.
    """
    try:
        # Construcción inicial de la consulta
        query = select(Solicitud)
        
        # Agrega condiciones dinámicamente basadas en los filtros
        if filtros.descripcion_solicitud:
            query = query.where(Solicitud.descripcion_solicitud.ilike(f"%{filtros.descripcion_solicitud}%"))
        
        if filtros.id_ciudadano_solicitud:
            query = query.where(Solicitud.id_ciudadano_solicitud == filtros.id_ciudadano_solicitud)
        
        # Ejecuta la consulta con los filtros aplicados
        result = await db.execute(query)
        solicitudes = result.scalars().all()

        return solicitudes
    except Exception as e:
        raise Exception(f"Error al filtrar solicitudes: {str(e)}")


async def create_solicitud(db: AsyncSession, solicitud_data: dict):
    try:
        nueva_solicitud = Solicitud(**solicitud_data)
        db.add(nueva_solicitud)
        await db.commit()
        await db.execute(
            text("SELECT setval('solicitud_id_solicitud_seq', (SELECT MAX(id_solicitud) FROM solicitud))")
        )
        
        await db.refresh(nueva_solicitud)
        return nueva_solicitud
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear solicitud: {str(e)}")


async def update_solicitud(db: AsyncSession, solicitud_id: int, solicitud_data: SolicitudUpdate):
    try:
        result = await db.execute(select(Solicitud).where(Solicitud.id_solicitud == solicitud_id))
        solicitud = result.scalar_one_or_none()
        if solicitud is None:
            return None

        update_data = solicitud_data.model_dump(exclude_unset=True)
        await db.execute(
            sql_update(Solicitud)
            .where(Solicitud.id_solicitud == solicitud_id)
            .values(**update_data)
        )
        await db.commit()
        await db.refresh(solicitud)
        return solicitud
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al actualizar solicitud: {str(e)}")


async def delete_solicitud(db: AsyncSession, solicitud_id: int):
    try:
        result = await db.execute(
            sql_delete(Solicitud)
            .where(Solicitud.id_solicitud == solicitud_id)
            .returning(Solicitud.id_solicitud)
        )
        deleted = result.scalar_one_or_none()
        await db.commit()
        return deleted is not None
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al eliminar solicitud: {str(e)}")
