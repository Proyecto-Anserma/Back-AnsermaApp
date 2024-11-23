from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, select, update as sql_update, delete as sql_delete
from .solicitud_db_modelo import Solicitud
from .solicitud_modelos import *

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


async def update_solicitud(db: AsyncSession, solicitud_id: int, solicitud_data: SolicitudBase):
    try:
        # Buscar la solicitud existente
        result = await db.execute(select(Solicitud).where(Solicitud.id_solicitud == solicitud_id))
        solicitud = result.scalar_one_or_none()
        if solicitud is None:
            return None  # Devuelve None si no se encuentra la solicitud

        # Preparar los datos para la actualización
        update_data = solicitud_data.model_dump(exclude_unset=True)

        # Aplicar los cambios en la base de datos
        await db.execute(
            sql_update(Solicitud)
            .where(Solicitud.id_solicitud == solicitud_id)
            .values(**update_data)
        )
        await db.commit()

        # Refrescar el objeto actualizado
        await db.refresh(solicitud)

        # Construir la respuesta sin duplicar el campo 'geolocalizacion'
        solicitud_dict = solicitud.__dict__.copy()  # Copiar los datos del objeto SQLAlchemy
        geolocalizacion = solicitud_dict.pop("geolocalizacion", None)  # Extraer geolocalización
        solicitud_response = SolicitudResponse(**solicitud_dict, geolocalizacion=geolocalizacion)

        return solicitud_response
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
