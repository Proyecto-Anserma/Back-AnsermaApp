from pydoc import text

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from .ciudadano_db_modelo import Ciudadano
from .ciudadano_modelos import *

async def filtrar_ciudadanos(
    db: AsyncSession, 
    filtros: CiudadanoFiltrar
):
    try:
        # Construcción inicial de la consulta
        query = select(Ciudadano)

        # Agrega condiciones dinámicamente basadas en los filtros
        if filtros.numero_identificacion_ciudadano:
            query = query.where(Ciudadano.numero_identificacion_ciudadano.ilike(f"%{filtros.numero_identificacion_ciudadano}%"))

        # Ejecuta la consulta con los filtros aplicados
        result = await db.execute(query)
        ciudadanos = result.scalars().all()

        return ciudadanos
    except Exception as e:
        raise Exception(f"Error al filtrar ciudadanos: {str(e)}")


async def create_ciudadano(db: AsyncSession, ciudadano_data: dict):
    try:
        nuevo_ciudadano = Ciudadano(**ciudadano_data)
        db.add(nuevo_ciudadano)
        await db.commit()
        await db.execute(
            text("SELECT setval('ciudadano_numero_identificacion_ciudadano_seq', (SELECT MAX(numero_identificacion_ciudadano) FROM ciudadano))")
        )
        await db.refresh(nuevo_ciudadano)
        return nuevo_ciudadano
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear ciudadano: {str(e)}")


async def update_ciudadano(db: AsyncSession, ciudadano_id: str, ciudadano_data: CiudadanoBase):
    try:
        # Buscar el ciudadano existente
        result = await db.execute(select(Ciudadano).where(Ciudadano.numero_identificacion_ciudadano == ciudadano_id))
        ciudadano = result.scalar_one_or_none()
        if ciudadano is None:
            return None  # Devuelve None si no se encuentra el ciudadano

        # Preparar los datos para la actualización
        update_data = ciudadano_data.model_dump(exclude_unset=True)

        # Asegurarse de que la geolocalización se incluya en los datos de actualización
        if ciudadano_data.geolocalizacion:
            update_data['geolocalizacion'] = ciudadano_data.geolocalizacion

        # Aplicar los cambios en la base de datos usando la función update de SQLAlchemy
        stmt = update(Ciudadano).where(Ciudadano.numero_identificacion_ciudadano == ciudadano_id).values(**update_data)
        await db.execute(stmt)
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
        raise HTTPException(status_code=400, detail=f"Error al actualizar ciudadano: {str(e)}")

async def delete_ciudadano(db: AsyncSession, ciudadano_id: int):
    """
    Elimina un ciudadano por su ID.
    """
    try:
        query = select(Ciudadano).where(Ciudadano.id == ciudadano_id)
        result = await db.execute(query)
        ciudadano = result.scalars().first()

        if not ciudadano:
            return False

        await db.delete(ciudadano)
        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        raise ValueError(f"Error al eliminar ciudadano: {str(e)}")
