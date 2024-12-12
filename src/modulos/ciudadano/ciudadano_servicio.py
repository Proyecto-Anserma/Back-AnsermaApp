from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import select, update as sql_update, delete as sql_delete
from geoalchemy2 import WKTElement
from geoalchemy2.elements import WKTElement
from shapely import wkt
from .ciudadano_db_modelo import Ciudadano
from .ciudadano_modelos import  CiudadanoBase, CiudadanoResponse, CiudadanosFiltrar
from sqlalchemy.orm import selectinload

async def get_ciudadanos(db: AsyncSession):
    result = await db.execute(select(Ciudadano))
    return result.scalars().all()

async def create_ciudadano(db: AsyncSession, ciudadano_data: dict):
    try:
        nuevo_ciudadano = Ciudadano(**ciudadano_data)
        db.add(nuevo_ciudadano)
        await db.commit()
        await db.refresh(nuevo_ciudadano)
        return nuevo_ciudadano
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear ciudadano: {str(e)}")

# async def update_ciudadano(db: AsyncSession, ciudadano_id: str, ciudadano_data: CiudadanoUpdate):
#     try:
#         geom_str = ciudadano_data.geolocalizacion
        
#         if geom_str.startswith('SRID='):
#             srid = int(geom_str.split(';')[0].replace('SRID=', ''))
#             wkt_str = geom_str.split(';')[1]
#         else:
#             srid = 4326
#             wkt_str = geom_str

#         update_data = ciudadano_data.model_dump()  
#         update_data['geolocalizacion'] = WKTElement(wkt_str, srid=srid) 
#         update_data['telefono_ciudadano'] = int(update_data['telefono_ciudadano'])
#         result = await db.execute(
#             sql_update(Ciudadano)
#             .where(Ciudadano.numero_identificacion_ciudadano == ciudadano_id)
#             .values(**update_data)
#             .returning(Ciudadano)
#         )
#         await db.commit()
#         updated_ciudadano = result.scalar_one_or_none()
#         return updated_ciudadano

#     except Exception as e:
#         await db.rollback()
#         raise Exception(f"Error al actualizar ciudadano: {str(e)}")


async def delete_ciudadano(db: AsyncSession, ciudadano_id: str):
    try:
        result = await db.execute(
            sql_delete(Ciudadano)
            .where(Ciudadano.numero_identificacion_ciudadano == ciudadano_id)
            .returning(Ciudadano.numero_identificacion_ciudadano)
        )
        deleted = result.scalar_one_or_none()
        await db.commit()
        return deleted is not None
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al eliminar ciudadano: {str(e)}")
    


async def filtrar_ciudadanos(
    db: AsyncSession, 
    filtros: CiudadanosFiltrar
):
    """
    Filtra ciudadanos por descripción y/o id_ciudadano_solicitud.
    Si no se proporcionan filtros, devuelve todas las ciudadanos.
    """
    try:
        # Construcción inicial de la consulta
        query = (
            select(Ciudadano)
            .options(selectinload(Ciudadano.genero)) 
            .options(selectinload(Ciudadano.pertenencia_etnica)) 
            .options(selectinload(Ciudadano.ubicacion)) 
        )
        
        # Agrega condiciones dinámicamente basadas en los filtros
        if filtros.numero_identificacion_ciudadano:
            query = query.where(Ciudadano.numero_identificacion_ciudadano.ilike(f"%{Ciudadano.numero_identificacion_ciudadano}%"))
        
        # Ejecuta la consulta con los filtros aplicados
        result = await db.execute(query)
        ciudadanos = result.scalars().all()

        return ciudadanos
    except Exception as e:
        raise Exception(f"Error al filtrar solicitudes: {str(e)}")
    
async def update_ciudadano(db: AsyncSession, numero_identificacion_ciudadano: str, ciudadano_data: CiudadanoBase):
    try:
        # Buscar ciudadanos
        result = await db.execute(select(Ciudadano).where(Ciudadano.numero_identificacion_ciudadano == numero_identificacion_ciudadano))
        ciudadano = result.scalar_one_or_none()
        if ciudadano is None:
            return None  # Devuelve None si no se encuentra la ciudadano

        # Preparar los datos para la actualización
        update_data = ciudadano_data.model_dump(exclude_unset=True)

        # Asegurarse de que la geolocalización se incluya en los datos de actualización
        if ciudadano_data.geolocalizacion:
            update_data['geolocalizacion'] = ciudadano_data.geolocalizacion

        # Aplicar los cambios en la base de datos
        await db.execute(
            sql_update(Ciudadano)
            .where(Ciudadano.numero_identificacion_ciudadano == numero_identificacion_ciudadano)
            .values(**update_data)
        )
        await db.commit()

        # Refrescar el objeto actualizado
        await db.refresh(ciudadano)

        # Construir la respuesta sin duplicar el campo 'geolocalizacion'
        ciudadano_dict = ciudadano.__dict__.copy()  # Copiar los datos del objeto SQLAlchemy
        geolocalizacion = ciudadano_dict.pop("geolocalizacion", None)  # Extraer geolocalización
        ciudadano_response = CiudadanoResponse(**ciudadano_dict, geolocalizacion=geolocalizacion)

        return ciudadano_response
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al actualizar solicitud: {str(e)}")