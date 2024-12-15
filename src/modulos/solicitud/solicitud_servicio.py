from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, select, update as sql_update, delete as sql_delete
from sqlalchemy.orm import selectinload
from .solicitud_db_modelo import Solicitud
from .solicitud_modelos import *
from src.modulos.estado_solicitud.estado_solicitud_db_modelo import EstadoSolicitud

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
        query = (
            select(Solicitud)
            .options(
                selectinload(Solicitud.tipo_solicitud),
                selectinload(Solicitud.ubicacion),
                selectinload(Solicitud.estados)
                .selectinload(EstadoSolicitud.estado)
            )
        )
        
        
        # Agrega condiciones dinámicamente basadas en los filtros
        if filtros.descripcion_solicitud:
            query = query.where(Solicitud.descripcion_solicitud.ilike(f"%{filtros.descripcion_solicitud}%"))
        
        if filtros.id_ciudadano_solicitud:
            query = query.where(Solicitud.id_ciudadano_solicitud == filtros.id_ciudadano_solicitud)
        
        # Ejecuta la consulta con los filtros aplicados
        result = await db.execute(query)
        solicitudes = result.unique().scalars().all()

        return solicitudes
    except Exception as e:
        raise Exception(f"Error al filtrar solicitudes: {str(e)}")


from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

async def create_solicitud(db: AsyncSession, solicitud_data: dict):
    try:
        # Crear la solicitud
        nueva_solicitud = Solicitud(**solicitud_data)
        db.add(nueva_solicitud)
        await db.flush()  # Para obtener el id_solicitud

        # Crear el estado inicial de la solicitud
        nuevo_estado = EstadoSolicitud(
            fecha_cambio_estado_solicitud=date.today(),
            observacion_solicitud="Se asignó con éxito",
            id_solicitud=nueva_solicitud.id_solicitud,
            id_estado=1
        )
        db.add(nuevo_estado)
        
        await db.commit()
        
        # Actualizar la secuencia
        await db.execute(
            text("SELECT setval('solicitud_id_solicitud_seq', (SELECT MAX(id_solicitud) FROM solicitud))")
        )
        
        # Obtener la solicitud con todas sus relaciones
        stmt = (
            select(Solicitud)
            .options(
                selectinload(Solicitud.tipo_solicitud),
                selectinload(Solicitud.ubicacion),
                selectinload(Solicitud.estados)
                .selectinload(EstadoSolicitud.estado)
            )
            .filter(Solicitud.id_solicitud == nueva_solicitud.id_solicitud)
        )
        
        result = await db.execute(stmt)
        solicitud_completa = result.unique().scalars().first()
        
        return solicitud_completa

    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear solicitud: {str(e)}")


async def update_solicitud(
    db: AsyncSession, 
    solicitud_id: int,
    solicitud_actualizada: SolicitudCreate
):
    try:
        # Convertir a diccionario y eliminar campos que no queremos actualizar
        update_data = solicitud_actualizada.model_dump(exclude_unset=True)
        
        # Eliminar campos que no corresponden a la tabla directamente
        campos_a_excluir = ['ubicacion', 'tipo_solicitud', 'estados']
        for campo in campos_a_excluir:
            update_data.pop(campo, None)
        
        # Actualizar la solicitud
        stmt = (
            sql_update(Solicitud)
            .where(Solicitud.id_solicitud == solicitud_id)
            .values(**update_data)
        )
        
        await db.execute(stmt)
        await db.commit()
        
        # Obtener la solicitud actualizada con sus relaciones
        stmt = (
            select(Solicitud)
            .options(
                selectinload(Solicitud.tipo_solicitud),
                selectinload(Solicitud.ubicacion),
                selectinload(Solicitud.estados)
                .selectinload(EstadoSolicitud.estado)
            )
            .where(Solicitud.id_solicitud == solicitud_id)
        )
        
        result = await db.execute(stmt)
        solicitud_actualizada = result.unique().scalars().first()
        
        if not solicitud_actualizada:
            return None
            
        return solicitud_actualizada
        
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

async def get_solicitud_by_id(db: AsyncSession, solicitud_id: int):
    stmt = (
        select(Solicitud)
        .options(
            selectinload(Solicitud.tipo_solicitud),
            selectinload(Solicitud.ubicacion),
            selectinload(Solicitud.estados)
            .selectinload(EstadoSolicitud.estado)
        )
        .where(Solicitud.id_solicitud == solicitud_id)
    )
    result = await db.execute(stmt)
    return result.unique().scalars().first()
