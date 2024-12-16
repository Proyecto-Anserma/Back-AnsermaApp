from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, update as sql_update, delete as sql_delete
from .cantidad_origen_ayuda_db_modelo import CantidadOrigenAyuda
from .cantidad_origen_ayuda_modelos import CantidadOrigenAyudaCreate

async def get_cantidades_origen_ayuda(db: AsyncSession):
    try:
        result = await db.execute(select(CantidadOrigenAyuda))
        return result.scalars().all()
    except Exception as e:
        raise Exception(f"Error al obtener cantidades de origen de ayuda: {str(e)}")
    

async def create_cantidad_origen_ayuda(
    db: AsyncSession, cantidad_origen_ayuda_data: CantidadOrigenAyudaCreate
):
    try:
        # Convertir el modelo Pydantic a diccionario
        data_dict = cantidad_origen_ayuda_data.model_dump(exclude_unset=True)
        
        # Si no se proporcionó fecha, usar la fecha actual
        if 'fecha_entrega_cantidad_origen_ayuda' not in data_dict or data_dict['fecha_entrega_cantidad_origen_ayuda'] is None:
            data_dict['fecha_entrega_cantidad_origen_ayuda'] = date.today()

        nueva_cantidad = CantidadOrigenAyuda(**data_dict)
        db.add(nueva_cantidad)
        await db.commit()

        # Actualizar la secuencia
        await db.execute(
            text("SELECT setval('cantidad_origen_ayuda_id_cantidad_origen_ayuda_seq', (SELECT MAX(id_cantidad_origen_ayuda) FROM cantidad_origen_ayuda))")
        )
        
        await db.refresh(nueva_cantidad)
        return nueva_cantidad
        
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear cantidad de origen ayuda: {str(e)}")
    

async def update_cantidad_origen_ayuda(
    db: AsyncSession, cantidad_origen_ayuda_id: int, cantidad_origen_ayuda_data: CantidadOrigenAyudaCreate
):
    """
    Actualiza una cantidad de origen de ayuda existente.

    :param db: Sesión de base de datos
    :param cantidad_origen_ayuda_id: ID de la cantidad de origen de ayuda a actualizar
    :param cantidad_origen_ayuda_data: Datos nuevos para actualizar
    :return: La cantidad de origen de ayuda actualizada o None si no se encuentra
    """
    try:
        result = await db.execute(
            sql_update(CantidadOrigenAyuda)
            .where(CantidadOrigenAyuda.id_cantidad_origen_ayuda == cantidad_origen_ayuda_id)
            .values(**cantidad_origen_ayuda_data.dict())
            .returning(CantidadOrigenAyuda)
        )
        updated_cantidad = result.scalar_one_or_none()
        if updated_cantidad:
            await db.commit()
            await db.refresh(updated_cantidad)
        return updated_cantidad
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al actualizar cantidad de origen de ayuda: {str(e)}")


async def delete_cantidad_origen_ayuda(db: AsyncSession, cantidad_origen_ayuda_id: int):
    try:
        result = await db.execute(
            sql_delete(CantidadOrigenAyuda)
            .where(CantidadOrigenAyuda.id_cantidad_origen_ayuda == cantidad_origen_ayuda_id)
            .returning(CantidadOrigenAyuda.id_cantidad_origen_ayuda)
        )
        deleted = result.scalar_one_or_none()
        await db.commit()
        return deleted is not None
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al eliminar cantidad de origen de ayuda: {str(e)}")
