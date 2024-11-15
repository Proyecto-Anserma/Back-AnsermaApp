from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import select, update as sql_update, delete as sql_delete
from geoalchemy2 import WKTElement
from geoalchemy2.elements import WKTElement
from shapely import wkt
from .ciudadano_db_modelo import Ciudadano
from .ciudadano_modelos import CiudadanoCreate, CiudadanoUpdate

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

async def update_ciudadano(db: AsyncSession, ciudadano_id: str, ciudadano_data: CiudadanoUpdate):
    try:
        # Verificamos si 'geolocalizacion' fue incluida en los datos de actualización
        geom_str = ciudadano_data.geolocalizacion
        
        if geom_str.startswith('SRID='):
            srid = int(geom_str.split(';')[0].replace('SRID=', ''))
            wkt_str = geom_str.split(';')[1]
        else:
            srid = 4326  # Asignamos un SRID por defecto si no está presente
            wkt_str = geom_str

        # Preparamos los datos para la actualización
        update_data = ciudadano_data.model_dump()  # Convertimos el modelo a diccionario
        update_data['geolocalizacion'] = WKTElement(wkt_str, srid=srid)  # Guardamos la geolocalizacion
        update_data['telefono_ciudadano'] = int(update_data['telefono_ciudadano'])  # Aseguramos que el teléfono sea un entero

        # Realizamos la actualización en la base de datos
        result = await db.execute(
            sql_update(Ciudadano)
            .where(Ciudadano.numero_identificacion_ciudadano == ciudadano_id)
            .values(**update_data)
            .returning(Ciudadano)
        )
        await db.commit()

        # Obtenemos el ciudadano actualizado
        updated_ciudadano = result.scalar_one_or_none()
        return updated_ciudadano

    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al actualizar ciudadano: {str(e)}")


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