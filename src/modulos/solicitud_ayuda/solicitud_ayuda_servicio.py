from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, update as sql_update, delete as sql_delete
from datetime import date, datetime
from .solicitud_ayuda_db_modelo import SolicitudAyuda
from .solicitud_ayuda_modelos import SolicitudAyudaCreate
from src.modulos.estado_solicitud.estado_solicitud_db_modelo import EstadoSolicitud
import logging

# Configurar logging
logger = logging.getLogger(__name__)

async def get_solicitudes_ayuda(db: AsyncSession):
    try:
        result = await db.execute(select(SolicitudAyuda))
        return result.scalars().all()
    except Exception as e:
        raise Exception(f"Error al obtener solicitudes de ayuda: {str(e)}")

async def create_solicitud_ayuda(db: AsyncSession, solicitud_ayuda_data: SolicitudAyudaCreate):
    try:
        # Crear la solicitud de ayuda
        logger.info(f"Creando solicitud de ayuda con datos: {solicitud_ayuda_data}")
        nueva_solicitud_ayuda = SolicitudAyuda(**solicitud_ayuda_data.model_dump())
        db.add(nueva_solicitud_ayuda)
        await db.flush()
        
        logger.info(f"Solicitud de ayuda creada con ID: {nueva_solicitud_ayuda.id_solicitud_ayuda}")

        # Crear el estado de la solicitud
        nuevo_estado_solicitud = EstadoSolicitud(
            fecha_cambio_estado_solicitud=datetime.today(),
            observacion_solicitud="Solicitud asignada con éxito",
            id_solicitud=solicitud_ayuda_data.id_solicitud,
            id_estado=2
        )
        
        logger.info(f"Creando estado de solicitud para solicitud ID: {solicitud_ayuda_data.id_solicitud}")
        db.add(nuevo_estado_solicitud)
        
        # Confirmar ambas operaciones
        await db.commit()
        logger.info("Transacción completada exitosamente")
        
        # Actualizar la secuencia
        await db.execute(
            text("SELECT setval('solicitud_ayuda_id_solicitud_ayuda_seq', (SELECT MAX(id_solicitud_ayuda) FROM solicitud_ayuda))")
        )
        
        await db.refresh(nueva_solicitud_ayuda)
        return nueva_solicitud_ayuda
        
    except Exception as e:
        logger.error(f"Error en create_solicitud_ayuda: {str(e)}")
        await db.rollback()
        raise Exception(f"Error al crear solicitud de ayuda y su estado: {str(e)}")

async def create_estado_solicitud(db: AsyncSession, id_solicitud: int):
    """Función auxiliar para crear el estado de la solicitud"""
    try:
        nuevo_estado = EstadoSolicitud(
            fecha_cambio_estado_solicitud=date.today(),
            observacion_solicitud="Solicitud asignada con éxito",
            id_solicitud=id_solicitud,
            id_estado=2
        )
        db.add(nuevo_estado)
        await db.flush()
        return nuevo_estado
    except Exception as e:
        logger.error(f"Error creando estado de solicitud: {str(e)}")
        raise

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

async def create_solicitud(db: AsyncSession, solicitud_data: dict):
    try:
        # Si no se proporciona fecha_entrega_solicitud_ayuda, se establece como None
        if 'fecha_entrega_solicitud_ayuda' not in solicitud_data:
            solicitud_data['fecha_entrega_solicitud_ayuda'] = None
            
        # Si no se proporciona foto_entrega_solicitud_ayuda, se establece como None    
        if 'foto_entrega_solicitud_ayuda' not in solicitud_data:
            solicitud_data['foto_entrega_solicitud_ayuda'] = None
            
        nueva_solicitud = SolicitudAyuda(**solicitud_data)
        db.add(nueva_solicitud)
        await db.commit()
        await db.refresh(nueva_solicitud)
        return nueva_solicitud
    except Exception as e:
        print(f"Error creando solicitud: {str(e)}")  # Debug
        await db.rollback()
        raise
