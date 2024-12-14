from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, update as sql_update, delete as sql_delete
from sqlalchemy.orm import selectinload, joinedload
from .estado_solicitud_db_modelo import EstadoSolicitud
from .estado_solicitud_modelos import EstadoSolicitudUpdate
from src.modulos.solicitud.solicitud_db_modelo import Solicitud
from typing import Optional

async def get_estado_solicitudes(db: AsyncSession):
    try:
        # Cargar todas las relaciones necesarias, incluyendo las relaciones anidadas
        query = (
            select(EstadoSolicitud)
            .options(
                joinedload(EstadoSolicitud.estado),
                joinedload(EstadoSolicitud.solicitud).joinedload(Solicitud.tipo_solicitud),
                joinedload(EstadoSolicitud.solicitud).joinedload(Solicitud.ubicacion)
            )
        )
        
        result = await db.execute(query)
        estados_solicitud = result.unique().scalars().all()
        
        # Asegurarse de que todas las relaciones estén cargadas
        for estado_solicitud in estados_solicitud:
            if estado_solicitud.solicitud:
                _ = estado_solicitud.solicitud.tipo_solicitud
                _ = estado_solicitud.solicitud.ubicacion
        
        return estados_solicitud
    except Exception as e:
        print(f"Error detallado: {str(e)}")  # Para debugging
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

async def get_ultimo_estado_solicitud(db: AsyncSession, id_solicitud: Optional[int] = None):
    try:
        # Iniciar la consulta base
        query = (
            select(EstadoSolicitud)
            .options(
                joinedload(EstadoSolicitud.estado),
                joinedload(EstadoSolicitud.solicitud).joinedload(Solicitud.tipo_solicitud),
                joinedload(EstadoSolicitud.solicitud).joinedload(Solicitud.ubicacion)
            )
        )
        
        # Si se proporciona id_solicitud, filtrar por él
        if id_solicitud is not None:
            query = query.where(EstadoSolicitud.id_solicitud == id_solicitud)
            
        # Ordenar por id_solicitud y fecha para obtener los últimos estados
        query = query.order_by(
            EstadoSolicitud.id_solicitud,
            EstadoSolicitud.fecha_cambio_estado_solicitud.desc()
        )
        
        result = await db.execute(query)
        estados = result.unique().scalars().all()
        
        # Filtrar para obtener solo el último estado de cada solicitud
        ultimos_estados = {}
        for estado in estados:
            if estado.id_solicitud not in ultimos_estados:
                ultimos_estados[estado.id_solicitud] = estado
                if estado.solicitud:
                    _ = estado.solicitud.tipo_solicitud
                    _ = estado.solicitud.ubicacion
        
        return list(ultimos_estados.values())
    except Exception as e:
        print(f"Error detallado: {str(e)}")
        raise Exception(f"Error al obtener el último estado de la solicitud: {str(e)}")
