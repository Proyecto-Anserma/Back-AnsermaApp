from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, update as sql_update, delete as sql_delete, func
from sqlalchemy.orm import selectinload, joinedload
from .estado_solicitud_db_modelo import EstadoSolicitud
from .estado_solicitud_modelos import EstadoSolicitudUpdate, ReporteSolicitudFiltro, ReporteEstadoResponse
from src.modulos.solicitud.solicitud_db_modelo import Solicitud
from typing import Optional, List
from datetime import date, datetime

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
        # Agregamos la fecha y hora actual al diccionario de datos
        estado_solicitud_data['fecha_cambio_estado_solicitud'] = datetime.now()
        
        nuevo_estado_solicitud = EstadoSolicitud(**estado_solicitud_data)
        db.add(nuevo_estado_solicitud)
        await db.flush()
        
        await db.commit()
        
        # Actualizar la secuencia
        await db.execute(
            text("SELECT setval('estado_solicitud_id_estado_solicitud_seq', (SELECT MAX(id_estado_solicitud) FROM estado_solicitud))")
        )
        
        # Obtener el estado_solicitud con sus relaciones
        stmt = (
            select(EstadoSolicitud)
            .options(
                selectinload(EstadoSolicitud.estado)
            )
            .where(EstadoSolicitud.id_estado_solicitud == nuevo_estado_solicitud.id_estado_solicitud)
        )
        
        result = await db.execute(stmt)
        estado_solicitud_completo = result.unique().scalars().first()
        
        return estado_solicitud_completo
        
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
    
async def get_reporte_solicitudes(db: AsyncSession, filtro: ReporteSolicitudFiltro) -> List[ReporteEstadoResponse]:
    try:
        # Iniciar la consulta base
        query = (
            select(EstadoSolicitud)
            .options(
                joinedload(EstadoSolicitud.estado),
                joinedload(EstadoSolicitud.solicitud)
            )
        )
        
        # Aplicar filtros si existen
        if filtro.fecha_inicio:
            query = query.where(EstadoSolicitud.fecha_cambio_estado_solicitud >= filtro.fecha_inicio)
        
        if filtro.fecha_fin:
            query = query.where(EstadoSolicitud.fecha_cambio_estado_solicitud <= filtro.fecha_fin)
            
        # Ordenar por id_solicitud y fecha para obtener los últimos estados
        query = query.order_by(
            EstadoSolicitud.id_solicitud,
            EstadoSolicitud.fecha_cambio_estado_solicitud.desc()
        )
        
        result = await db.execute(query)
        estados = result.unique().scalars().all()
        
        # Obtener solo el último estado de cada solicitud
        ultimos_estados = {}
        for estado in estados:
            if estado.id_solicitud not in ultimos_estados:
                ultimos_estados[estado.id_solicitud] = estado

        # Contar solicitudes por id_estado
        conteo_estados = {}
        for estado in ultimos_estados.values():
            if filtro.id_estado_solicitud and estado.id_estado != filtro.id_estado_solicitud:
                continue
            conteo_estados[estado.id_estado] = conteo_estados.get(estado.id_estado, 0) + 1

        # Convertir a formato de respuesta
        return [
            ReporteEstadoResponse(
                id_estado_solicitud=id_estado,
                cantidad_solicitudes=cantidad
            )
            for id_estado, cantidad in conteo_estados.items()
        ]

    except Exception as e:
        print(f"Error detallado: {str(e)}")
        raise Exception(f"Error al obtener el reporte de solicitudes: {str(e)}")
